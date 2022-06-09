"""
Extract tracks from the BOX_STEREO_TRACK aux data.
"""

import argparse
import json
from pathlib import Path
from typing import List, Union

from lib.models import Track, TrackEvent, AuxData, Box


def parse_tracks(log):
    track_dict = {}
    for event_idx, event in enumerate(log):
        try:
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
                    
                    # Check timestamp difference from last event
                    last_event_in_track = track.events[-1]
                    timestamp_diff = event_timestamp - last_event_in_track.timestamp
                    
                    # If timestamp difference is too large (> 12 hours), assume this is a new track
                    # Assign a new track ID as 1000000 + the track ID
                    if timestamp_diff > 12 * 3600:
                        track_id = int(1e6 + track_id)
                        track = Track(
                            id = track_id,
                            class_name=box_left['class_name'],
                            events=[]
                        )
                        track_dict[track_id] = track
                            
                
                track.events.append(TrackEvent(
                    timestamp=event_timestamp,
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


def extract_tracks(log_path: Path, output_path: Path, quiet: bool = False) -> List[Track]:
    log = json.loads(log_path.read_text())
    
    track_dict = parse_tracks(log)
    
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
