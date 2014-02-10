from PySide import QtGui, QtCore

class ControlPanel(QtGui.QWidget):
	def __init__(self, device, parent):
		super(ControlPanel, self).__init__(parent, QtCore.Qt.Window)

		self.device = device
		self.setWindowTitle(self.device.name)