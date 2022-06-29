"""
Plotly plotting utilities for representing tracks.
"""

import plotly.graph_objects as go
from timesignal import EventOrchestra, EventSignal

from lib.models import Track


def track_to_single_trace(track: Track):
    """
    Create a single trace from a track object.
    """
    return go.Scatter(
        x=[ev.x_mm for ev in track.events],
        y=[ev.y_mm for ev in track.events],
        mode='lines+markers',
        name=f'{track.id}'
    )


STATE_COLORS = {
    0: 'gray',
    1: 'green',
    2: 'yellow',
    3: 'red',
}
STATE_NAMES = {
    0: 'idle',
    1: 'search',
    2: 'acquire',
    3: 'track'
}
def track_to_trace_list(track: Track, states: list):
    """
    Create a list of traces from a track object, with changing colors to indicate different states.
    """
    # Identify spans of events in each state
    spans = []
    for event, state in zip(track.events, states):
        if spans and spans[-1][0] == state:
            spans[-1][1].append(event)
        else:
            if spans:
                spans[-1][1].append(event)  # last event in span = first event in next span
            spans.append([state, [event]])
    
    # Create traces for each state span
    traces = []
    for state, events in spans:
        traces.append(go.Scatter(
            x=[ev.x_mm for ev in events],
            y=[ev.y_mm for ev in events],
            mode='lines+markers',
            line=dict(color=STATE_COLORS[state]),
            name=f'{track.id} - {state}'
        ))
    
    return traces


def track_orchestra_to_trace_list(track_id: int, track_signal: EventOrchestra, supervisor_signal: EventSignal):
    x_signal = track_signal.get_signal('x')
    y_signal = track_signal.get_signal('y')
    datetimes, x_values = zip(*x_signal.values)
    y_values = y_signal.interpolate_datetimes(datetimes)
    state_numbers = supervisor_signal.interpolate_datetimes(datetimes)
    points = list(zip(x_values, y_values))
    
    # Identify spans of events in each state
    spans = []
    for point, state in zip(points, state_numbers):
        if spans and spans[-1][0] == state:
            spans[-1][1].append(point)
        else:
            if spans:
                spans[-1][1].append(point)  # last point in span = first point in next span
            spans.append([state, [point]])
    
    # Create traces for each state span
    traces = []
    for state, points in spans:
        traces.append(go.Scatter(
            x=[p[0] for p in points],
            y=[p[1] for p in points],
            mode='lines+markers',
            line=dict(color=STATE_COLORS[state]),
            name=f'{track_id} - {STATE_NAMES[state]}'
        ))
    
    return traces
