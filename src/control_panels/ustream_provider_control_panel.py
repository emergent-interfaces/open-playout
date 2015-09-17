from PySide import QtGui
from control_panel import ControlPanel
from functools import partial


class UstreamProviderControlPanel(ControlPanel):
    def __init__(self, device, parent):
        super(UstreamProviderControlPanel, self).__init__(device, parent)
        self.init_ui()

    def init_ui(self):
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)

        self.url = QtGui.QLineEdit(self.device.url_and_key.get_value()[0])
        self.key = QtGui.QLineEdit(self.device.url_and_key.get_value()[1])

        formLayout = QtGui.QFormLayout()
        formLayout.addRow('URL:', self.url)
        formLayout.addRow('Key:', self.key)

        vbox.addLayout(formLayout)

        self.setKeyAndUrl = QtGui.QPushButton('Update Connection')
        self.setKeyAndUrl.clicked.connect(self.change_url_and_key)
        self.device.url_and_key.changed.connect(self.url_and_key_changed)

        vbox.addWidget(self.setKeyAndUrl)

    def change_url_and_key(self):
        self.device.url_and_key.set_value([self.url.text(), self.key.text()])

    def url_and_key_changed(self, new_value):
        self.url.setText(new_value[0])
        self.key.setText(new_value[1])
