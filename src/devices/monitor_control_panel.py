from PySide import QtGui
from control_panel import ControlPanel
from functools import partial

class MonitorControlPanel(ControlPanel):
    def __init__(self, device, parent):
        super(MonitorControlPanel, self).__init__(device, parent)
        self.init_ui()

    def init_ui(self):
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)

        formLayout = QtGui.QFormLayout()
        vbox.addLayout(formLayout)

        x, y = self.device.location.get_value()
        width, height = self.device.size.get_value()

        lineX = QtGui.QSpinBox()
        lineY = QtGui.QSpinBox()
        lineWidth = QtGui.QSpinBox()
        lineHeight = QtGui.QSpinBox()

        for spinBox in [lineX, lineY, lineWidth, lineHeight]:
            spinBox.setRange(-10000, 10000)

        lineX.setValue(int(x))
        lineY.setValue(int(y))
        lineWidth.setValue(int(width))
        lineHeight.setValue(int(height))

        formLayout.addRow("x", lineX)
        formLayout.addRow("y", lineY)
        formLayout.addRow("width", lineWidth)
        formLayout.addRow("height", lineHeight)

        lineX.valueChanged.connect(self.change_location)
        lineY.valueChanged.connect(self.change_location)
        lineWidth.valueChanged.connect(self.change_size)
        lineHeight.valueChanged.connect(self.change_size)
        self.device.location.changed.connect(self.location_changed)
        self.device.size.changed.connect(self.size_changed)

        self.lineX = lineX
        self.lineY = lineY
        self.lineWidth = lineWidth
        self.lineHeight = lineHeight

        # Full screen buttons
        fullScreenButtonsLayout = QtGui.QHBoxLayout()
        vbox.addLayout(fullScreenButtonsLayout)

        desktopWidget = QtGui.QDesktopWidget()
        for i in range(desktopWidget.screenCount()):
            button = QtGui.QPushButton("Screen " + str(i+1))
            button.clicked.connect(partial(self.make_full_screen, i))
            fullScreenButtonsLayout.addWidget(button)

    def change_location(self, new_value):
        new_location = (self.lineX.value(), self.lineY.value())
        self.device.location.set_value(new_location)

    def change_size(self, new_value):
        new_size = (self.lineWidth.value(), self.lineHeight.value())
        self.device.size.set_value(new_size)

    def location_changed(self, new_value):
        x, y = new_value
        self.lineX.setValue(x)
        self.lineY.setValue(y)

    def size_changed(self, new_value):
        width, height = new_value
        self.lineWidth.setValue(width)
        self.lineHeight.setValue(height)

    def make_full_screen(self, screen_index):
        screenGeometry = QtGui.QDesktopWidget().screenGeometry(screen_index)
        x, y, width, height = screenGeometry.getRect()
        self.device.location.set_value((x,y))
        self.device.size.set_value((width, height))