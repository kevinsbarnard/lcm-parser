# ML-Tracking LCM Log Analysis Workspace

This project is an in-progress analysis workspace for the ML-Tracking LCM logs from May 24-25, 2021.

## Relevant components
- `data/` directory contains all relevant data files, except for the base LCM logs. These are available separately on Atlas.
    - Data is further split by encoding: `json`, `text`, `lcm`, `pickle`, `csv`
    - A manifest for the files in each data subdirectory are provided in the respective `MANIFEST.md` file.
- `lib/` contains all relevant Python libraries.
- Higher-level data processing/visualization is handled in the `.ipynb` Jupyter notebooks.
- Utility scripts are provided as `.py` files in the root directory.

## Requirements
- Python 3.8+
- Jupyter
- [timesignal](https://github.com/kevinsbarnard/timesignal)
- External packages in `requirements.txt`; install with:
```bash
pip install -r requirements.txt
```

## Important notes
- The original LCM logs have timestamps in Pacific Daylight Time, i.e. UTC-7. Timestamps are converted to UTC before processing for consistency.
- LCM log timestamps are recorded in microseconds. Timestamps are converted to seconds (scaled by 1e-6) before processing.
- The original LCM log `BOX_STEREO_TRACK` events were generated without the `track.py` `--all_tracks` flag, and thus are missing portions of the track data as well as other tracks. To correct this, the `track.py` was re-run with the `--all_tracks` flag to generate the full track data. The inputs (`BOX_STEREO` events) and outputs (`BOX_STEREO_TRACK` events) are provided in `data/lcm/`.

## Workflow
The overall workflow is as follows:
1. **Identify relevant LCM logs.** The paths to May 24-25 log files are included in `data/text/may_24_25_lcmlog_paths.txt`.
2. **Parse relevant LCM log events into JSON.** As LCM logs are non-indexed octet streams, they are not ideal for analysis. Therefore, the LCM log events are parsed into JSON objects as an intermediate representation. Much of this functionality is housed in `lib.parse`.
3. **Collect BOX_STEREO_TRACK events into tracks.** All events are listed flat in the JSON, but are keyed by channel. For easier analysis, events from the `BOX_STERO_TRACK` channel are parsed separately and grouped into `lib.models.Track` objects. The parsed track objects (from the `track.py` re-run) are available in `data/json/may_24_25_tracks.json`.
4. **Orchestrate the supervisor, vehicle, and track events.** This is where the `timesignal` library comes into play; it is used to collect the relevant events into a single, interpolable, datetime-keyed representation. The orchestra is generated in `orchestrate.ipynb` and stored in `data/pickle/orchestra.pkl`. An orchestra (`timesignal.EventOrchestra`) is a recursively-composed set of key-value pairs, where each key is a string and each value is either another orchestra (`timesignal.EventOrchestra`) or a signal (`timesignal.EventSignal`).
5. **Perform orchestra queries to extract synchronized data.** The resulting orchestra can be efficiently queried (interpolated) at any included datetime(s) to provide synchronized data across all relevant channels (signals). For example, this is done to generate the `data/csv/` datasets.
6. **Visualize.** WIP.
