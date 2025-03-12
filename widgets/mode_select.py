from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QRadioButton, QButtonGroup

class ModeSelect(QGroupBox):
    def __init__(self, option_list=["None"]):
        super().__init__("Mode Selection")
        
        self.layout = QVBoxLayout()
        self.button_group = QButtonGroup(self)
        self.option_list = option_list
        self.__add_options()
        self.setLayout(self.layout)

    def __add_options(self):
        for option in self.option_list:
            option_radio = QRadioButton(option)
            self.button_group.addButton(option_radio)
            self.layout.addWidget(option_radio)

    def get_selected_mode(self):
        for button in self.button_group.buttons():
            if button.isChecked():
                return button.text().lower()
        return None
