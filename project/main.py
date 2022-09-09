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
