import argparse
from pathlib import Path
import sys
from typing import Optional

import json
import progressbar

from lcm_reader import Event, LogExtractor
import mwt


def decode(event: Event, cls):
    """
    Decode an event into a native Python object
    """
    if not event.data:
        event.read_data()
    
    return cls.decode(event.data)


def to_dict(obj) -> dict:
    """
    Encode an object into a Python dictionary using slots
    """
    if hasattr(obj, '__slots__'):
        return {k: to_dict(getattr(obj, k)) for k in obj.__slots__}
    elif isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_dict(v) for v in obj]
    else:
        return obj


def parse(event: Event, cls_map: dict) -> Optional[dict]:
    """
    Parse an event into a dict using a given class map
    """
    if event.channel not in cls_map:
        return None
    
    cls = cls_map[event.channel]
    return to_dict(decode(event, cls))


def load_class_map(path: str) -> dict:
    """
    Load the class map from a given path
    """
    with open(path, 'r') as f:
        return {k: getattr(mwt, v) for k, v in json.load(f).items() if v is not None}


def parse_log(log_path: Path, class_map_path: Path, output_path: Path, quiet: bool = False) -> None:
    """
    Parse a log file into a JSON file
    """
    def print_quiet(*args, **kwargs):
        if not quiet:
            print(*args, **kwargs)
    
    # Load class map
    class_map = load_class_map(str(class_map_path))
    
    # Index log
    print_quiet(f'Indexing {log_path}...', end='')
    sys.stdout.flush()
    log_extractor = LogExtractor(str(log_path))
    print_quiet('done')
    
    # Parse events into list of dicts
    event_gen = (parse(ev, class_map) for ev in log_extractor.index)
    if not quiet:
        event_gen = progressbar.progressbar(event_gen, max_value=len(log_extractor.index), redirect_stdout=True)
    print_quiet(f'Parsing {log_path}...')
    parsed_dicts = []
    for event, event_dict in zip(log_extractor.index, event_gen):
        if event_dict is not None:
            parsed_dict = {
                'meta': {
                    'channel': event.channel,
                    'event_number': event.header.event_number,
                    'timestamp': event.header.timestamp
                },
                'event': event_dict
            }
            parsed_dicts.append(parsed_dict)

    print_quiet(f'Writing {output_path}...', end='')
    sys.stdout.flush()
    with open(output_path, 'w') as f:
        json.dump(parsed_dicts, f, indent=2)
    print_quiet('done')


def main():
    parser = argparse.ArgumentParser(description='Parse a log file')
    parser.add_argument('log', type=str, help='Path to the log file')
    parser.add_argument('classmap', type=str, help='Path to the class map file')
    parser.add_argument('-o', '--output', type=str, help='Path to the output file')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress output')
    args = parser.parse_args()
    
    # Parse log path
    log_path = Path(args.log)
    if not log_path.is_file():
        parser.error(f'Invalid log path: {log_path}')
        
    # Parse class map
    class_map_path = Path(args.classmap)
    if not class_map_path.is_file():
        parser.error(f'Invalid class map path: {class_map_path}')
    
    # Parse output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(log_path.name + '.json')
    
    parse_log(log_path, class_map_path, output_path, quiet=args.quiet)


if __name__ == '__main__':
    main()
