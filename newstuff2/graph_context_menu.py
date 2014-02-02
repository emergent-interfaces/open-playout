from PySide import QtGui, QtCore


class GraphContextMenu(QtGui.QMenu):
	def __init__(self):
		super(GraphContextMenu, self).__init__()
		self.addMenu(GraphSourcesMenu())
		self.addMenu(GraphSwitchesMenu())
		self.addMenu(GraphOutputsMenu())
		

class GraphSourcesMenu(QtGui.QMenu):
	def __init__(self):
		super(GraphSourcesMenu, self).__init__()
		self.setTitle('Sources')
		self.addAction("Video Test Generator")
		self.addAction("V4L2 Source")

class GraphSwitchesMenu(QtGui.QMenu):
	def __init__(self):
		super(GraphSwitchesMenu, self).__init__()
		self.setTitle('Switches')
		self.addAction("4 Input Video Switcher")

class GraphOutputsMenu(QtGui.QMenu):
	def __init__(self):
		super(GraphOutputsMenu, self).__init__()
		self.setTitle('Outputs')
		self.addAction("Screen Output")		