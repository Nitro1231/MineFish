# event.py
#
# Copyright 2020 Nitro. All Rights Reserved.
#
# Developer: Nitro (admin@nitrostudio.dev)
# Blog: https://blog.nitrostudio.dev
# Discord: Nitro#1781
# GitHub: https://github.com/Nitro1231/MineFish
#
# Version: 4.0.0
# Last Modified: Saturday, September 10, 2022, at 7:23 PM. (KST)
#
# This project is licensed under the GNU Affero General Public License v3.0;
# you may not use this file except in compliance with the License.


class Event:
    events = []
    count = 0
    # logger = None

    def link(self, event) -> None:
        Event.events.append(event)
        # Event.logger(event)

    def call(self) -> None:
        Event.count += 1
        for e in Event.events:
            e()
        # Event.logger(f'[Event] Total of {len(Event.events)} has been called.')
