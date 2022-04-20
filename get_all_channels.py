from dataclasses import dataclass
import json
from pathlib import Path
from lcm_reader import LogExtractor, LogReader


@dataclass
class LCMLog:
    path: str
    location: str
    platform: str
    recorded_date: str


with open('lcmlogs.json', 'r') as f:
    lcmlogs = [LCMLog(**l) for l in json.load(f)]


all_channels = set()
for log in lcmlogs:
    print(log.path)
    extractor = LogExtractor(log.path)
    all_channels |= set(ev.channel for ev in extractor.index)

with open('all_channels.json', 'w') as f:
    json.dump(list(all_channels), f, indent=2, sort_keys=True)