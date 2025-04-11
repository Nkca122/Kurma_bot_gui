from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QRadioButton, QButtonGroup

class ModeSelect(QGroupBox):
    def __init__(self, option_list=["None"]):
        super().__init__()
        self.layout = QVBoxLayout()
        self.button_group = QButtonGroup(self)
        self.option_list = option_list
        self.__add_options()
        self.setLayout(self.layout)

        self.setStyleSheet(
            """
            QGroupBox {
                background-color: #2b2b2b;
                border: none;
                border-radius: 10px;
                padding: 8px;
                margin-top: 4px;
            }

            QRadioButton {
                spacing: 6px;
                font-size: 14px;
                color: #dddddd;
                padding: 6px 10px;
                border-radius: 6px;
            }

            QRadioButton:hover {
                background-color: #3a3a3a;
            }

            QRadioButton:checked {
                background-color: #0078d7;
                color: white;
            }
        """
        )

    def __add_options(self):
        for i, option in enumerate(self.option_list):
            option_radio = QRadioButton(option)
            if i == 0:
                option_radio.setChecked(True)
            self.button_group.addButton(option_radio)
            self.layout.addWidget(option_radio)

    def get_selected_mode(self):
        for button in self.button_group.buttons():
            if button.isChecked():
                return button.text().lower()
        return None
