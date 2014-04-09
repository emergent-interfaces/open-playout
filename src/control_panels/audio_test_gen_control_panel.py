from PySide import QtGui, QtCore
from control_panel import ControlPanel
import math


class AudioTestGenControlPanel(ControlPanel):
    def __init__(self, device, parent):
        super(AudioTestGenControlPanel, self).__init__(device, parent)
        self.init_ui()

    def init_ui(self):
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)
        self.setMinimumWidth(400)

        slider0 = QtGui.QScrollBar()
        slider0.setTracking(True)
        slider0.setRange(0, 1000)
        slider0.setOrientation(QtCore.Qt.Horizontal)
        slider0.setValue(self.freq_to_pos(self.device.freqs.get_value()[0]))
        slider0.valueChanged.connect(self.change_freqs)
        self.vbox.addWidget(slider0)
        self.slider0 = slider0

        slider1 = QtGui.QScrollBar()
        slider1.setTracking(True)
        slider1.setRange(0, 1000)
        slider1.setOrientation(QtCore.Qt.Horizontal)
        slider1.setValue(self.freq_to_pos(self.device.freqs.get_value()[1]))
        slider1.valueChanged.connect(self.change_freqs)
        self.vbox.addWidget(slider1)
        self.slider1 = slider1

        self.device.freqs.changed.connect(self.freqs_changed)

    def change_freqs(self):
        self.device.freqs.set_value([self.pos_to_freq(self.slider0.value()),
                                     self.pos_to_freq(self.slider1.value())])

    def freqs_changed(self, data):
        self.slider0.setValue(self.freq_to_pos(data[0]))
        self.slider1.setValue(self.freq_to_pos(data[1]))

    a = 303.0
    b = 0.05

    def freq_to_pos(self, freq):
        return self.a * math.log10(self.b * freq)

    def pos_to_freq(self, pos):
        return math.pow(10.0, pos / self.a) / self.b
