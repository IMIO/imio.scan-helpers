#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the imio.scan_helpers distribution (https://github.com/IMIO/imio.scan_helpers).
# Copyright (c) 2023 IMIO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from config import get_bundle_dir
from config import PARAMS_FILE_NAME
from datetime import datetime
from logger import close_logger
from logger import log
from utils import copy_sub_files
from utils import get_last_dated_backup_dir
from utils import get_main_backup_dir
from utils import get_parameter
from utils import get_scan_profiles_dir
from utils import read_dir
from utils import send_log_message
from utils import stop

import argparse
import os
import shutil


# Argument parsing
parser = argparse.ArgumentParser()
# parser.add_argument("-v", "--version", action="store_true", dest="version", help="Show version")
# parser.add_argument("-r", "--release", dest="release", help="Get this release")
ns = parser.parse_args()

log.info("Starting restore script")
bundle_dir = get_bundle_dir()
params_file = os.path.join(bundle_dir, PARAMS_FILE_NAME)
client_id = get_parameter(params_file, "CLIENT_ID")
try:
    main_backup_dir = get_main_backup_dir()
    dated_backup_dir = get_last_dated_backup_dir(main_backup_dir)
    if not dated_backup_dir:
        stop(f"No dated backup dir in  '{main_backup_dir}'", client_id=client_id)
    prof_dirs = read_dir(dated_backup_dir, with_path=False, only_folders=True)
    if not prof_dirs:
        stop(f"No profiles found in '{dated_backup_dir}'", client_id=client_id)
    main_prof_dir = get_scan_profiles_dir()
    for prof_dir in prof_dirs:
        adir = os.path.join(main_prof_dir, prof_dir)
        if os.path.exists(adir):
            shutil.rmtree(adir)
    copy_sub_files(dated_backup_dir, main_prof_dir, files=prof_dirs)
except Exception as ex:
    send_log_message(f"General error in profiles-restore script '{ex}'", client_id)

log.info("Finished restore script")
close_logger()
