"""
Extract points from all tracks in an EventOrchestra to a CSV file for loading into a Pandas DataFrame.
"""

import argparse
import pickle
from pathlib import Path

import pandas as pd


SUPERVISOR_KEY = 'supervisor'
STATE_NUMBER_KEY = 'state_number'
ALL_TRACKS_KEY = 'all_tracks'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('orchestra_file', type=Path)
    parser.add_argument('output_file', type=Path)
    parser.add_argument('stride', type=int)
    
    args = parser.parse_args()
    orchestra_file = args.orchestra_file
    output_file = args.output_file
    stride = args.stride
    
    if not orchestra_file.suffix == '.pkl':
        parser.error(f'{orchestra_file} is not a pickle file')
    
    if not output_file.suffix == '.csv':
        parser.error(f'{args.output_file} is not a CSV file')

    if stride < 1:
        parser.error(f'{stride} is not a positive integer')
    
    # Load orchestra
    with orchestra_file.open('rb') as f:
        orchestra = pickle.load(f)
    
    # Get relevant orchestras/signals
    supervisor_orchestra = orchestra.get_signal(SUPERVISOR_KEY)
    state_number_signal = supervisor_orchestra.get_signal(STATE_NUMBER_KEY)
    all_tracks_orchestra = orchestra.get_signal(ALL_TRACKS_KEY)
    
    dataframe_tuples = []
    for track_id in all_tracks_orchestra._elements:
        # Get the track orchestra
        track_orchestra = all_tracks_orchestra.get_signal(track_id)
        
        # Get the coordinate signals
        x = track_orchestra.get_signal('x')
        y = track_orchestra.get_signal('y')
        z = track_orchestra.get_signal('z')
        
        # Get the key datetimes
        datetimes = [val[0] for val in x.values]
        
        # Append tuples of (track_id, datetime, x, y, z, state)
        new_tuples = [(track_id, dt, x[dt], y[dt], z[dt], state_number_signal[dt]) for dt in datetimes][::stride]
        dataframe_tuples.extend(new_tuples)

    # Compose DataFrame
    df = pd.DataFrame(dataframe_tuples, columns=['track_id', 'datetime', 'x', 'y', 'z', 'state'])

    # Save DataFrame to CSV
    df.to_csv(str(output_file), index=False)


if __name__ == '__main__':
    main()


