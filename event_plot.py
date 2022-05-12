from datetime import datetime
from collections import defaultdict
import json

from plotly.subplots import make_subplots
import plotly.graph_objects as go

LOG_FILE = 'lcmlog-2021-05-24.00.json'

START = 0
END = 9999999

def timestamp_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp / 1e6)


with open(LOG_FILE) as f:
    events = json.load(f)

INCLUDE_CHANNELS = [
    'ML_CFG',
    'SUPERVISOR_CFG',
    'MWT_TARGET',
    'EXT_TARGET_3'
]
events_by_channel = defaultdict(list)
for event in events[START:END]:
    channel = event['meta']['channel']
    if channel in INCLUDE_CHANNELS:
        events_by_channel[channel].append(event)


def make_scatter(channel: str, events: list):
    x = [timestamp_to_datetime(event['meta']['timestamp']) for event in events]
    y = [0 for _ in events]
    hover_text = [json.dumps(event['event'], indent=2).replace('\n', '<br>') for event in events]
    
    return go.Scatter(x=x, y=y, mode='markers', marker_size=10, name=channel, hovertext=hover_text)
    

fig = make_subplots(rows=len(events_by_channel), cols=1, subplot_titles=tuple(events_by_channel.keys()), shared_xaxes=True)
for idx, (channel, events) in enumerate(events_by_channel.items()):
    fig.add_trace(make_scatter(channel, events), row=idx+1, col=1)

fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=False, 
                 zeroline=True, zerolinecolor='black', zerolinewidth=1,
                 showticklabels=False)
# fig.update_layout(height=200, plot_bgcolor='white')

fig.show()
