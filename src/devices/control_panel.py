from PySide import QtGui

class ControlPanel(QtGui.QMainWindow):
	def __init__(self, device, parent):
		super(ControlPanel, self).__init__(parent)
		self.device = device