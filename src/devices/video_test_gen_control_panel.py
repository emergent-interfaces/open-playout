from PySide import QtGui
from control_panel import ControlPanel

class VideoTestGenControlPanel(ControlPanel):
    def __init__(self, device, parent):
        super(VideoTestGenControlPanel, self).__init__(device, parent)
        self.init_ui()

    def init_ui(self):
        hbox = QtGui.QHBoxLayout()
        self.setLayout(hbox)

        patternSelector = QtGui.QComboBox()
        patternSelector.addItem("SMPTE")
        patternSelector.addItem("snow")
        patternSelector.addItem("black")
        patternSelector.addItem("white")
        patternSelector.addItem("red")
        patternSelector.addItem("green")
        patternSelector.addItem("blue")
        patternSelector.addItem("checkers 1")
        patternSelector.addItem("checkers 2")
        patternSelector.addItem("checkers 4")
        patternSelector.addItem("checkers 8")
        patternSelector.addItem("circular")
        patternSelector.addItem("blink")
        patternSelector.addItem("SMPTE 75")
        patternSelector.addItem("zone plate")
        patternSelector.addItem("gamut")
        patternSelector.addItem("chroma zone plate")
        patternSelector.addItem("solid")
        patternSelector.addItem("ball")
        patternSelector.addItem("SMPTE 100")
        patternSelector.addItem("bar")
        patternSelector.addItem("pinwheel")
        patternSelector.addItem("spokes")
        hbox.addWidget(patternSelector)

        patternSelector.setCurrentIndex(self.device.pattern.get_value())

        patternSelector.currentIndexChanged.connect(self.change_pattern)
        self.patternSelector = patternSelector

        self.device.pattern.changed.connect(self.pattern_changed)

    def change_pattern(self, index):
        self.device.pattern.set_value(index)

    def pattern_changed(self, pattern):
        self.patternSelector.setCurrentIndex(pattern)

    def closeEvent(self, event):
        self.device.remove_control_panel(self)