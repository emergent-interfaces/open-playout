from PySide import QtGui, QtCore

class Display(QtGui.QWidget):
	def __init__(self, parent, monitor):
		super(Display, self).__init__(parent, QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
		self.monitor = monitor

		x, y = monitor.location.get_value()
		width, height = monitor.size.get_value()
		self.setWindowTitle(self.monitor.name)
		self.setGeometry(x, y, width, height)
		self.show()

	def showEvent(self, event):
		self.monitor.set_window_id(self.winId())	

	def set_location(self, x, y):
		width, height = self.monitor.size.get_value()
		self.setGeometry(x, y, width, height)

	def set_size(self, width, height):
		x, y = self.monitor.location.get_value()
		self.setGeometry(x, y, width, height)

	# todo Figure out how to update location and size via mouse dragging
	# without causing recursion.
	# def moveEvent(self, event):
	# 	self.monitor.location.set_value(self.pos().toTuple())