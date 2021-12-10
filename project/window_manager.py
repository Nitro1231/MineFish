# window_handler.py
#
# Copyright 2020 Nitro. All Rights Reserved.
#
# Developer: Nitro (admin@nitrostudio.dev)
# Blog: https://blog.nitrostudio.dev
# Discord: Nitro#1781
# GitHub: https://github.com/Nitro1231/MineFish
#
# Version: 4.0.0
# Last Modified: Monday, December 6, 2021 at 11:11 AM. (PDT)
#
# This project is licensed under the GNU Affero General Public License v3.0;
# you may not use this file except in compliance with the License.

import pygetwindow


def get_window_by_filter(filter: dict()) -> 'Win32Window' or None:
    windows = pygetwindow.getAllTitles()

    include = False
    exclude = True
    for title in windows:
        for text in filter['include']:
            if text in title:
                include = True
                break
        for text in filter['exclude']:
            if text in title:
                include = False
                break
        if include and exclude:
            return pygetwindow.getWindowsWithTitle(title)[0]
    return None


def get_window_size(handle: 'Win32Window') -> tuple():
    x1, y1, x2, y2 = handle._getWindowRect()
    width, height = handle.width, handle.height
    return x1, y1, x2, y2, width, height
