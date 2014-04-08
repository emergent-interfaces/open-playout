from PySide import QtGui
from control_panel import ControlPanel


class AudioTestGenControlPanel(ControlPanel):
    def __init__(self, device, parent):
        super(AudioTestGenControlPanel, self).__init__(device, parent)
        self.init_ui()

    def init_ui(self):
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)

        slider1 = QtGui.QScrollBar()
        self.vbox.addWidget(slider1)
