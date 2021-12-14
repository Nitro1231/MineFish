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


def get_matched_window(match_list: dict()) -> 'Win32Window' or None:
    '''
    Grab all windows and find the window that is matched with the given 
    condition. Return the 'Win32Window' object if the window is matched 
    with the condition; return 'None' otherwise.

    Parameters:
         • match_list: The dictionary that includes lists named 
         'include' and 'exclude' that indicates words that should be filtered.
    '''

    windows = pygetwindow.getAllWindows()

    for window in windows:
        if match_text(window.title, match_list):
            return window
    return None


def match_text(text: str, match_list: dict()) -> bool:
    '''
    Match the text with a given condition and return a boolean value 
    that indicates whether they are matched.

    Parameters:
         • text: The target text.
         • match_list: The dictionary that includes lists named 
         'include' and 'exclude' that indicates words that should be filtered.
    '''

    include = False
    exclude = True

    for word in match_list['include']:
        if word in text:
            include = True
            break

    for word in match_list['exclude']:
        if word in text:
            exclude = False
            break

    return include and exclude


def get_window_size(handle: 'Win32Window') -> tuple():
    '''
    Get and return the window's left, top, width, and height.

    Parameters:
         • handle: The 'Win32Window' object.
    '''

    left, top = handle.left, handle.top
    width, height = handle.width, handle.height
    return left, top, width, height


# TEST:
# match = {
#     'include': ['Minecraft'],
#     'exclude': ['Launcher']
# }

# window = get_matched_window(match)

# print(window)
# print(get_window_size(window))
