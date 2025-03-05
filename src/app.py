# app.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
import os
from dotenv import load_dotenv
from utils import run_script

load_dotenv()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('MR Exporter')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        instructions = QLabel(
            "1. Create a <a href='{}'>Google Sheet</a> with a tab named in the format `MM.YYYY` (e.g., `11.2023`) "
            "and headers: `giturl`, `date`, `title`.<br><br>"
            "2. Refresh the project in <a href='{}'>Sheety</a> after creating the tab.<br><br>"
            "3. Press 'Run Script' to execute the code.".format(
                os.getenv("GOOGLE_SHEET_URL"), os.getenv("SHEETY_DASHBOARD_URL")
            )
        )
        instructions.setFont(QFont('Helvetica', 14))
        instructions.setOpenExternalLinks(True)
        layout.addWidget(instructions)

        self.run_button = QPushButton('Run Script', self)
        self.run_button.setFont(QFont('Helvetica', 14))
        self.run_button.clicked.connect(run_script)
        layout.addWidget(self.run_button)

        self.setLayout(layout)
