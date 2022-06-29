"""
Filter LCM log file events by channel, and write to a new file.
"""

import argparse
from io import BufferedIOBase
from typing import Iterable, Optional, Tuple


LCM_SYNCWORD = (0xEDA1DA01).to_bytes(4, 'big')
EVENT_NUMBER_BYTES = 8
TIMESTAMP_BYTES = 8
CHANNEL_LENGTH_BYTES = 4
DATA_LENGTH_BYTES = 4
HEADER_BYTES = 4 + EVENT_NUMBER_BYTES + TIMESTAMP_BYTES + CHANNEL_LENGTH_BYTES + DATA_LENGTH_BYTES


TARGET_CHANNEL = 'BOX_STEREO'


def read_one(file: BufferedIOBase) -> Optional[Tuple[int, int]]:
    event_start_idx = file.tell()

    # Ensure syncword
    syncword = file.read(4)
    assert syncword == LCM_SYNCWORD

    # Read header data
    event_number = int.from_bytes(file.read(EVENT_NUMBER_BYTES), 'big')
    timestamp = int.from_bytes(file.read(TIMESTAMP_BYTES), 'big')
    channel_length = int.from_bytes(file.read(CHANNEL_LENGTH_BYTES), 'big')
    data_length = int.from_bytes(file.read(DATA_LENGTH_BYTES), 'big')

    # Read channel
    channel = file.read(channel_length).decode()
    
    # Compute event end index
    event_end_idx = event_start_idx + HEADER_BYTES + channel_length + data_length
    
    # Skip to next event
    file.seek(event_end_idx)

    if channel == TARGET_CHANNEL:
        return event_start_idx, event_end_idx


def read_all(file: BufferedIOBase) -> Iterable[Tuple[int, int]]:
    while True:
        try:
            bounds = read_one(file)
            if bounds is not None:
                yield bounds
        except:
            break


def copy_one(input_file: BufferedIOBase, output_file: BufferedIOBase, start_idx: int, end_idx: int):
    input_file.seek(start_idx)
    output_file.write(input_file.read(end_idx - start_idx))


def copy_all(input_file: BufferedIOBase, output_file: BufferedIOBase):
    for start_idx, end_idx in read_all(input_file):
        copy_one(input_file, output_file, start_idx, end_idx)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input_file', type=argparse.FileType('rb'))
    parser.add_argument('output_file', type=argparse.FileType('wb'))
    parser.add_argument('-c', '--channel', default=TARGET_CHANNEL)

    # Parse args
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

    # Filter/copy events
    copy_all(input_file, output_file)
    
    # Close files
    output_file.close()
    input_file.close()


if __name__ == '__main__':
    main()
