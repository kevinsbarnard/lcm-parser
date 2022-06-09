import pickle
from typing import Iterable, List, Set, Tuple
import numpy as np

import plotly.express as px
import pandas as pd

from lib.models import Track


def get_tracks() -> List[Track]:
    with open('tracks.pkl', 'rb') as f:
        return pickle.load(f)


def get_points(track: Track) -> List[Tuple[float, float, float]]:
    points = list(set(
        (
            ev.x_mm,
            ev.y_mm,
            ev.z_mm
        )
        for ev in track.events
    ))
    
    return points


def get_points_df(track: Track):
    points = get_points(track)
    
    df = pd.DataFrame(
        points,
        columns=['x', 'y', 'z']
    )
    
    return df


def make_heatmap(track: Track):
    df = get_points_df(track)
    
    fig = px.density_heatmap(df, x='x', y='y')
    
    return fig


def make_scatter(track: Track):
    df = get_points_df(track)
    
    fig = px.scatter(df, x='x', y='y')
    
    return fig


def make_scatter_3d(track: Track):
    df = get_points_df(track)
    
    fig = px.scatter_3d(df, x='x', y='y', z='z')
    
    return fig


def track_to_rows(track: Track) -> Iterable[tuple]:
    for idx, ev in enumerate(track.events[::50]):
        yield track.id, idx, track.class_name, ev.x_mm, ev.y_mm, ev.z_mm, ev.width_mm, ev.height_mm


def tracks_to_df(tracks: Iterable[Track]) -> pd.DataFrame:
    all_rows = []
    for track in tracks:
        all_rows.extend(track_to_rows(track))
    
    df = pd.DataFrame(
        all_rows,
        columns=['track_id', 'event_idx', 'class_name', 'x', 'y', 'z', 'width', 'height']
    )
    
    return df


def main():
    print('Loading tracks')
    tracks = get_tracks()
    
    print('Sorting tracks')
    tracks.sort(key=lambda t: t.duration.total_seconds(), reverse=True)
    
    # print('Collecting all points')
    # all_points = []
    # for track in tracks[:100]:
    #     all_points.extend(get_points(track))
    
    # points_arr = np.array(all_points)
    # distances = np.linalg.norm(points_arr, axis=1)
    
    # d = np.abs(distances - np.median(distances))
    # mdev = np.std(d)
    # s = d/mdev if mdev else 0
    
    # print(f'Total points: {len(all_points)}')
    
    # filtered_points = points_arr[s<1, :]  # within 1 standard deviation
    
    # print(f'Filtered points: {len(filtered_points)}')
    
    # df = pd.DataFrame(
    #     filtered_points,
    #     columns=['x', 'y', 'z']
    # )
    
    # fig = px.density_heatmap(df, x='x', y='y')
    
    print('Generating dataframe')
    df = tracks_to_df(tracks[:100])
    
    df['size'] = (df['width'] * df['height'] / 1e3).clip(lower=1, upper=5).round().astype(int)
    
    print('Generating figure')
    bound_size = 1e3
    fig = px.scatter(
        df, 
        x='x', y='y',
        animation_frame='event_idx', 
        animation_group='track_id', 
        range_x=[-bound_size, bound_size], 
        range_y=[-bound_size, bound_size],
        color='class_name',
        size='size',
    )
    
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
    
    fig.show()


if __name__ == '__main__':
    main()
