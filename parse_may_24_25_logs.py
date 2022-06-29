"""
Parse the May 24-25 LCM logs (on Atlas) into JSON.
"""

from pathlib import Path

from lib.parse import parse_log


LOG_PATH_STRINGS = r'''\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.00
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.01
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.02
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.03
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.04
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.05
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.06
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.07
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.08
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.09
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.10
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.11
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.12
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.13
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.14
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.15
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.16
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.17
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.24.2021\lcmlog-2021-05-24.18
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.00
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.01
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.02
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.03
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.04
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.05
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.06
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.07
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.08
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.09
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.10
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.11
\\atlas.shore.mbari.org\BioInspirLabData\210517-25_RC_MiniROV\lcmLogs.May.25.2021\lcmlog-2021-05-25.12'''.splitlines()

LOG_PATHS = list(map(Path, LOG_PATH_STRINGS))

# SUPERVISOR_CFG type was changed part way through. Split paths into two partitions.
SPLIT_IDX = 19
OLD_CFG_LOG_PATHS = LOG_PATHS[:SPLIT_IDX]
NEW_CFG_LOG_PATHS = LOG_PATHS[SPLIT_IDX:]

JSON_DIR = Path('data/json/')
OLD_CFG_PATH = JSON_DIR / 'ml_tracking_channel_map.json'
NEW_CFG_PATH = JSON_DIR / 'ml_tracking_channel_map_alt.json'

# Where to save the output data
OUTPUT_DIR = Path('data/json/parsed_lcm/')
OUTPUT_DIR.mkdir(exist_ok=True)

OLD_CFG_PATH_LIST = len(OLD_CFG_LOG_PATHS) * [OLD_CFG_PATH]
NEW_CFG_PATH_LIST = len(NEW_CFG_LOG_PATHS) * [NEW_CFG_PATH]

def get_output_path(log_path):
    return OUTPUT_DIR / (log_path.name + '.json')

# Parse
for log_path, cfg_path in zip(LOG_PATHS, OLD_CFG_PATH_LIST + NEW_CFG_PATH_LIST):
    output_path = get_output_path(log_path)
    if output_path.exists():
        print(f'Skipping {log_path} as its target output file {output_path} already exists.')
        continue
    print(f'Extracting {log_path} to {output_path}')
    parse_log(log_path, cfg_path, output_path)
