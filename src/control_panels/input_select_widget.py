from PySide import QtCore, QtGui
from functools import partial


class InputSelectWidget(QtGui.QWidget):
    clicked = QtCore.Signal(int)

    def __init__(self, inputs, default=0, parent=None, f=0):
        super(InputSelectWidget, self).__init__(parent, f)
        self.inputs = inputs
        self.init_ui()

        self.active = default
        self.buttons[default].setChecked(True)

    def init_ui(self):
        hbox = QtGui.QHBoxLayout()

        self.buttons = []
        for i in range(self.inputs):
            button = QtGui.QPushButton(str(i))
            button.setCheckable(True)
            button.clicked.connect(partial(self.buttonClicked, i))

            self.buttons.append(button)
            hbox.addWidget(button)

        self.setLayout(hbox)

    def buttonClicked(self, button_index):
        if self.active == button_index:
            self.buttons[button_index].setChecked(True)

        for i, button in enumerate(self.buttons):
            if i != button_index:
                button.setChecked(False)

        self.active = button_index
        self.clicked.emit(self.active)

    def setPressed(self, button_index):
        for i, button in enumerate(self.buttons):
            if i != button_index:
                button.setChecked(False)
            else:
                button.setChecked(True)


if __name__ == "__main__":
    import sys

    def clickHandler(index):
        print index

    app = QtGui.QApplication(sys.argv)

    window = QtGui.QWidget()
    windowLayout = QtGui.QHBoxLayout()
    window.setLayout(windowLayout)

    testWidget = InputSelectWidget(4)
    testWidget.clicked.connect(clickHandler)
    windowLayout.addWidget(testWidget)

    window.show()
    sys.exit(app.exec_())
