from PySide import QtGui, QtCore

class ControlPanel(QtGui.QWidget):
    def __init__(self, device, parent):
        super(ControlPanel, self).__init__(parent, QtCore.Qt.Window)

        self.device = device
        self.setWindowTitle(self.device.name)

    def center_at(self, pos):
        x, y = pos.toTuple()
        x = x - self.width() / 2.0
        y = y - self.height() / 2.0
        self.move(x, y)