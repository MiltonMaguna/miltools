# -----------------------------------------------------------------------------
# Editor Milton Maguna / milton.maguna@gmail.com
# 1.0.0 - open folder for project care giver olvs  -  03/28/2023
#
# from scripts.custom_projects.care_giver_olvs.main import *
# open_folder(get_path_renders())
# open_folder(get_path_helpers())
# -----------------------------------------------------------------------------
import os
import sys
from pathlib import Path
import nuke

from custom_projects.care_giver_olvs.config_paths import PATHS


def get_name_shot():
    return nuke.root().name().split('/')[-3]


def get_path_assets():
    return Path(PATHS['assets'])


def get_path_renders():
    return Path(PATHS["renders"]) / get_name_shot()


def get_path_projects():
    return Path(PATHS["base_projects"])


def get_path_prerenders():
    return Path(PATHS["base_projects"]) / get_name_shot() / "prerenders"


def get_path_helpers():
    return Path(PATHS["base_projects"]) / get_name_shot() / "helpers"


def open_folder(path):

    try:
        print(f'opening {path}')

        if sys.platform == 'darwin':
            os.system(f'open "{path}"')
        elif sys.platform == 'win32':
            os.system(f'start explorer "{path}"')
    except Exception:
        print(f'failed!{path}')
