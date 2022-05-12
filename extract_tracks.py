"""
Extract tracks from the BOX_STEREO_TRACK aux data.
"""

import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Union

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class AuxDataState:
    """
    Units are all millimeters.
    """
    x: float
    y: float
    z: float
    w: float
    h: float


@dataclass_json
@dataclass
class AuxData:
    track_id: str
    state: AuxDataState
    association_score: float
    iou: float
    pixel_error: float


@dataclass_json
@dataclass
class Box:
    x: float
    y: float
    width: float
    height: float


@dataclass_json
@dataclass
class TrackEvent:
    timestamp: datetime
    
    # Image-space boxes
    box_left: Box
    box_right: Box
    
    # Position in robot frame
    x_meters: float
    y_meters: float
    z_meters: float
    
    # Size in robot frame
    width_meters: float
    height_meters: float
    
    # Track score (-100 to 100)
    score: int
    
    # Box association metadata
    association_score: float
    iou: float
    pixel_error: float


@dataclass_json
@dataclass
class Track:
    id: int
    class_name: str
    events: List[TrackEvent]
    
    @property
    def sorted_events(self) -> List[TrackEvent]:
        return sorted(self.events, key=lambda e: e.timestamp)
    
    @property
    def start_timestamp(self) -> datetime:
        return self.sorted_events[0].timestamp
    
    @property
    def end_timestamp(self) -> datetime:
        return self.sorted_events[-1].timestamp
    
    @property
    def duration(self) -> timedelta:
        return self.end_timestamp - self.start_timestamp


def extract_tracks(log_path: Path, output_path: Path, quiet: bool = False) -> List[Track]:
    log = json.loads(log_path.read_text())
    
    track_dict = {}
    try:
        for event in log:
            if event['meta']['channel'] != 'BOX_STEREO_TRACK':
                continue
            
            # Event data
            data = event['event']
            
            # Event timestamp
            event_timestamp = event['meta']['timestamp'] / 1e6
            
            for box_left, box_right in zip(data['left_boxes']['boxes'], data['right_boxes']['boxes']):
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
                    timestamp=event_timestamp,
                    box_left=Box(box_left['left'], box_left['top'], box_left['width'], box_left['height']),
                    box_right=Box(box_right['left'], box_right['top'], box_right['width'], box_right['height']),
                    x_meters=aux_data.state.x,
                    y_meters=aux_data.state.y,
                    z_meters=aux_data.state.z,
                    width_meters=aux_data.state.w,
                    height_meters=aux_data.state.h,
                    score=int(box_left['scores'][0]),
                    association_score=aux_data.association_score,
                    iou=aux_data.iou,
                    pixel_error=aux_data.pixel_error
                ))
    except Exception as e:
        pass
    
    sorted_tracks = sorted(list(track_dict.values()), key=lambda t: t.start_timestamp)
    track_dicts = [t.to_dict() for t in sorted_tracks]
    
    output_path.write_text(json.dumps(track_dicts, indent=2))


def load_tracks(track_file: Union[Path, str]) -> List[Track]:
    track_file = Path(track_file)
    if not track_file.is_file():
        raise FileNotFoundError(f'Track file not found: {track_file}')
    
    track_dicts = json.loads(track_file.read_text())
    tracks = [Track.from_dict(d) for d in track_dicts]
    del track_dicts
    return tracks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log_json', type=Path, help='Path to the parsed log JSON file')
    parser.add_argument('-o', '--output', type=Path, default=None, help='Path to the output file')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress output')
    
    args = parser.parse_args()
    
    log_json = args.log_json
    
    if not log_json.is_file():
        parser.error(f'Invalid log JSON path: {args.log_json}')
    elif not log_json.suffix == '.json':
        parser.error(f'File is not .json: {args.log_json}')
    
    extract_tracks(log_json, args.output if args.output is not None else log_json.with_suffix('.tracks.json'), quiet=args.quiet)


if __name__ == '__main__':
    main()
