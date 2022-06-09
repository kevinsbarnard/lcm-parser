import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import pickle
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from timesignal import EventOrchestra, EventSignal

from scripts.extract_tracks import parse_tracks

JSON_DIR = Path('extracted_logs/')
JSON_FILES = list(JSON_DIR.glob('*.json'))

TZ = timezone(timedelta(hours=-8))

# Read all events from all JSON files
print('Reading all events into memory...', end='', flush=True)
ALL_EVENTS = []
for json_file in JSON_FILES:
    with json_file.open('r') as f:
        events = json.load(f)
        ALL_EVENTS.extend(events)
print('done')

# Key by channel
print('Keying events by channel...', end='', flush=True)
EVENTS_BY_CHANNEL = defaultdict(list)
for event in ALL_EVENTS:
    EVENTS_BY_CHANNEL[event['meta']['channel']].append(event)
print('done')


def timestamp_to_datetime(ts: float) -> datetime:
    return datetime.fromtimestamp(ts, tz=TZ).astimezone(tz=timezone.utc)


def get_datetime(ev: dict) -> datetime:
    return timestamp_to_datetime(ev['meta']['timestamp'] / 1e6)


def get_extractor(*keys: str, map: Optional[dict] = None):
    def extract(ev: dict) -> Tuple[datetime, float]:
        v = ev['event']
        for k in keys:
            v = v[k]
        if map is not None:
            v = map[v]
        return get_datetime(ev), float(v)
    return extract


extractor_spec = {
    'SUPERVISOR_CFG': {
        'search_timeout': get_extractor('search_timeout'),
        'acquire_timeout': get_extractor('acquire_timeout'),
        'track_timeout': get_extractor('track_timeout'),
        'track_duration': get_extractor('track_duration'),
        'state_number': get_extractor('state_number'),
    },
    'MWT_CONTROL_STAT': {
        'x_enabled': get_extractor('is_x_effort_enabled'),
        'x_setpoint': get_extractor('x_traj', 'set_point'),
        'x_cmd': get_extractor('x_control', 'cmd'),
        'x_measure': get_extractor('x_control', 'measure'),
        'y_enabled': get_extractor('is_y_effort_enabled'),
        'y_setpoint': get_extractor('y_traj', 'set_point'),
        'y_cmd': get_extractor('y_control', 'cmd'),
        'y_measure': get_extractor('y_control', 'measure'),
        'z_enabled': get_extractor('is_z_effort_enabled'),
        'z_setpoint': get_extractor('z_traj', 'set_point'),
        'z_cmd': get_extractor('z_control', 'cmd'),
        'z_measure': get_extractor('z_control', 'measure'),
        'yaw_cmd': get_extractor('yaw_control', 'cmd'),
        'yaw_measure': get_extractor('yaw_control', 'measure'),
        'pilot_enabled': get_extractor('is_pilot_enabled'),
    },
    'MWT_SEARCH_STAT': {
        'x_mode': get_extractor('x_mode'),
        'x_effort_cmd': get_extractor('x_effort_cmd'),
        'y_mode': get_extractor('y_mode'),
        'y_effort_cmd': get_extractor('y_effort_cmd'),
        'z_mode': get_extractor('z_mode'),
        'z_effort_cmd': get_extractor('z_effort_cmd'),
        'yaw_mode': get_extractor('yaw_mode'),
        'yaw_effort_cmd': get_extractor('yaw_effort_cmd'),
        'control_mode': get_extractor('control_mode'),
    }
}


def make_event_orchestra(root_key) -> EventOrchestra:
    return EventOrchestra({
        key: EventSignal(map(extractor, EVENTS_BY_CHANNEL[root_key]), interpolation='nearest')
        for key, extractor in extractor_spec[root_key].items()
    })

print('Creating event orchestras for basic signals...', end='', flush=True)
supervisor_config_eo = make_event_orchestra('SUPERVISOR_CFG')
control_status_eo = make_event_orchestra('MWT_CONTROL_STAT')
search_status_eo = make_event_orchestra('MWT_SEARCH_STAT')
print('done')

print('Parsing tracks...', end='', flush=True)
track_dict = parse_tracks(ALL_EVENTS)
print('done')

print('Freeing memory...', end='', flush=True)
del ALL_EVENTS
del EVENTS_BY_CHANNEL
print('done')


def extract_track_event_signal(track, attr, interpolation='nearest') -> EventSignal:
    return EventSignal(((timestamp_to_datetime(e.timestamp), getattr(e, attr)) for e in track.events), interpolation=interpolation)


print('Extracting track signals...', end='', flush=True)
tracks_orchestra = EventOrchestra({
    str(track_id): EventOrchestra({
        'x': extract_track_event_signal(track, 'x_mm', interpolation='linear'),
        'y': extract_track_event_signal(track, 'y_mm', interpolation='linear'),
        'z': extract_track_event_signal(track, 'z_mm', interpolation='linear'),
        'width': extract_track_event_signal(track, 'width_mm', interpolation='linear'),
        'height': extract_track_event_signal(track, 'height_mm', interpolation='linear'),
        'score': extract_track_event_signal(track, 'score'),
    })
    for track_id, track in track_dict.items()
})
print('done')

root_orchestra = EventOrchestra({
    'supervisor': supervisor_config_eo,
    'control': control_status_eo,
    'search': search_status_eo,
    'tracks': tracks_orchestra,
})

print('Writing to file...', end='', flush=True)
with open('orchestra.pkl', 'wb') as f:
    pickle.dump(root_orchestra, f)
print('done')
