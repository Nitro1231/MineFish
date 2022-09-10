# main.py
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


import sys
import event
import update
import minefish
import update_gui
import minefish_gui
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    minefish = minefish.MineFish()
    event.Event().link(minefish.load_setting)
    event.Event().link(minefish.load_language)
    
    minefish_gui = minefish_gui.MineFishGUI(minefish)

    update_status, update_info = update.check_update()
    if update_status == True:
        update_gui = update_gui.UpdateGUI(minefish, update_info)

    sys.exit(app.exec())
