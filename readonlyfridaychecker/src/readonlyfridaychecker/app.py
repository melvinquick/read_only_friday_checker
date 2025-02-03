"""
This checks to see if today is Read Only Friday.
"""

import importlib.metadata
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
)

from readonlyfridaychecker.rof_api_checker import RofApiChecker


class ReadOnlyFridayChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.show()

        # * Set window default settings
        self.setWindowTitle("Read Only Friday Checker")
        self.setFixedSize(300, 150)

        # * Create widgets
        self.rof_check = QPushButton("Is it read-only Friday? \nPress me to find out!")
        self.rof_check.setFixedSize(280, 130)
        self.rof_check.setFont(self.set_font())

        # * Create layout
        self.page = QVBoxLayout()
        self.page.addWidget(self.rof_check)

        self.gui = QWidget()
        self.gui.setLayout(self.page)

        self.setCentralWidget(self.gui)

        # * Define connections
        self.rof_check.pressed.connect(self.check_rof)

        # * Apply theme to window
        self.apply_theme()

    def check_rof(self):
        rof = RofApiChecker()
        (
            self.rof_check.setText("Yes! \nDon't change anything!")
            if rof.get_response().json()["readonly"] == True
            else self.rof_check.setText("Nope. \nChange away!")
        )

    def apply_theme(self):
        self.main_stylesheet = f"""
            background-color: #2e3440;
            color: #eceff4;
            border: 1px solid #434c5e;
            border-radius: 4px;
            padding: 2px 4px;
            """
        self.widget_stylesheet = f"""
            background-color: #4c566a;
            """
        self.setStyleSheet(self.main_stylesheet)
        self.rof_check.setStyleSheet(self.widget_stylesheet)

    def set_font(self):
        font = QFont()
        font.setPointSize(12)
        return font


def main():
    # Linux desktop environments use an app's .desktop file to integrate the app
    # in to their application menus. The .desktop file of this app will include
    # the StartupWMClass key, set to app's formal name. This helps associate the
    # app's windows to its menu item.
    #
    # For association to work, any windows of the app must have WMCLASS property
    # set to match the value set in app's desktop file. For PySide6, this is set
    # with setApplicationName().

    # Find the name of the module that was used to start the app
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib.metadata.metadata(app_module)

    QApplication.setApplicationName(metadata["Formal-Name"])

    app = QApplication(sys.argv)
    main_window = ReadOnlyFridayChecker()
    sys.exit(app.exec())
