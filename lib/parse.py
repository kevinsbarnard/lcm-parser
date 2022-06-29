"""
Parsing utilities.
"""

import json
from pathlib import Path
from typing import Optional, Dict, List

import mwt
from lib.lcm_reader import Event, LogExtractor
from lib.models import ParsedEvent, Track, TrackEvent, AuxData, Box
from lib.timestamp import lcm_timestamp_to_seconds, pdt_timestamp_seconds_to_utc_datetime


def decode_event(event: Event, cls):
    """
    Decode an event into a native Python object.
    """
    if not event.data:
        event.read_data()
    
    return cls.decode(event.data)


def object_to_dict(obj) -> dict:
    """
    Encode an object into a Python dictionary using slots. Brittle.
    """
    if hasattr(obj, '__slots__'):
        return {k: object_to_dict(getattr(obj, k)) for k in obj.__slots__}
    elif isinstance(obj, dict):
        return {k: object_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [object_to_dict(v) for v in obj]
    else:
        return obj


def parse_event(event: Event, cls) -> Optional[dict]:
    """
    Parse an event into a dict using a given generated LCM class.
    If cls is None, return None.
    """
    if cls is None:
        return None
    
    return object_to_dict(decode_event(event, cls))


def load_class_map(path: str) -> dict:
    """
    Load the class map from a given path.
    """
    with open(path, 'r') as f:
        return {k: getattr(mwt, v) for k, v in json.load(f).items() if v is not None}


def parse_log(log_path: Path, class_map_path: Path, output_path: Path) -> None:
    """
    Parse a log file into a JSON file.
    """
    # Ensure Path objects
    log_path = Path(log_path)
    class_map_path = Path(class_map_path)
    output_path = Path(output_path)
    
    # Load class map
    class_map = load_class_map(str(class_map_path))
    
    # Index log
    log_extractor = LogExtractor(str(log_path))
    
    # Parse events into list of dicts
    event_gen = (parse_event(ev, class_map.get(ev.channel, None)) for ev in log_extractor.index)
    parsed_dicts = []
    for event, event_dict in zip(log_extractor.index, event_gen):
        if event_dict is not None:
            parsed_dict = {  # Corresponds to lib.models.ParsedEvent
                'meta': {
                    'channel': event.channel,
                    'event_number': event.header.event_number,
                    'timestamp': event.header.timestamp
                },
                'event': event_dict
            }
            parsed_dicts.append(parsed_dict)

    # Write to file
    with open(output_path, 'w') as f:
        json.dump(parsed_dicts, f, indent=2)


def parse_tracks(parsed_events: List[ParsedEvent]) -> Dict[int, Track]:
    """
    Parse BOX_STEREO_TRACK channel parsed events into a dict of integer track ID -> Track.
    """
    track_dict = {}
    for event_idx, parsed_event in enumerate(parsed_events):
        try:
            if parsed_event.meta.channel != 'BOX_STEREO_TRACK':
                continue
            
            # Event data
            event = parsed_event.event
            
            # Event datetime, in UTC
            event_utc_datetime = pdt_timestamp_seconds_to_utc_datetime(lcm_timestamp_to_seconds(parsed_event.meta.timestamp))
            
            for box_left, box_right in zip(event['left_boxes']['boxes'], event['right_boxes']['boxes']):
                aux_data: AuxData = AuxData.from_json(box_left['aux'])
                track_id = int(aux_data.track_id)
                if track_id not in track_dict:
                    track = Track(
                        id=track_id, 
                        class_name=box_left['class_name'], 
                        events=[]
                    )
                    track_dict[track_id] = track
                else:
                    track = track_dict[track_id]
                
                track.events.append(TrackEvent(
                    timestamp=event_utc_datetime,
                    box_left=Box(box_left['left'], box_left['top'], box_left['width'], box_left['height']),
                    box_right=Box(box_right['left'], box_right['top'], box_right['width'], box_right['height']),
                    x_mm=aux_data.state.x,
                    y_mm=aux_data.state.y,
                    z_mm=aux_data.state.z,
                    width_mm=aux_data.state.w,
                    height_mm=aux_data.state.h,
                    score=int(box_left['scores'][0]),
                    association_score=aux_data.association_score,
                    iou=aux_data.iou,
                    pixel_error=aux_data.pixel_error
                ))
        except Exception as e:
            print(f'Error parsing event {event_idx}: {e}')
    
    return track_dict
