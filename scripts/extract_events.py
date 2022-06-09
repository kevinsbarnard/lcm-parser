import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pathlib import Path

from scripts.parse import parse_log



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

OLD_CFG_LOG_PATHS = LOG_PATHS[:19]
NEW_CFG_LOG_PATHS = LOG_PATHS[19:]

OLD_CFG_PATH = 'extra_json/mlt_channels.json'
NEW_CFG_PATH = 'extra_json/mlt_channels_new.json'

OUTPUT_DIR = Path('extracted_logs/')
OUTPUT_DIR.mkdir(exist_ok=True)

OLD_CFG_PATH_LIST = len(OLD_CFG_LOG_PATHS) * [OLD_CFG_PATH]
NEW_CFG_PATH_LIST = len(NEW_CFG_LOG_PATHS) * [NEW_CFG_PATH]

def get_output_path(log_path):
    return OUTPUT_DIR / (log_path.name + '.json')

for log_path, cfg_path in list(zip(LOG_PATHS, OLD_CFG_PATH_LIST + NEW_CFG_PATH_LIST))[19:]:
    output_path = get_output_path(log_path)
    print(f'Extracting {log_path} to {output_path}')
    parse_log(log_path, cfg_path, output_path)
