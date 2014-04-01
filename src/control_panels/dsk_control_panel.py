from PySide import QtGui
from control_panel import ControlPanel

class DskControlPanel(ControlPanel):
    def __init__(self, device, parent):
        super(DskControlPanel, self).__init__(device, parent)
        self.init_gui()

    def init_gui(self):
        hbox = QtGui.QHBoxLayout()
        self.setLayout(hbox)

        button = QtGui.QPushButton('Select File')
        hbox.addWidget(button)

        button.clicked.connect(self.change_file)

        self.fader = QtGui.QSlider()
        self.fader.setTracking(True)
        self.fader.setRange(0, 100)
        self.fader.setValue(self.device.alpha.get_value()*100)
        self.device.alpha.changed.connect(self.alpha_changed)
        self.fader.valueChanged.connect(self.change_alpha)

        hbox.addWidget(self.fader)


    def change_file(self):
        file_name, selected_filter = QtGui.QFileDialog.getOpenFileName(self, 'Image File', '.', 'Files (*.svg *.png)')

        if file_name:
            self.device.file.set_value(file_name)

    def change_alpha(self, value):
        self.device.alpha.set_value(value/100.0)

    def alpha_changed(self, alpha):
        self.fader.setValue(alpha*100)