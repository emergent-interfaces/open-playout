from PySide import QtGui, QtCore
from node_types import VideoTestGenNode, V4L2SourceNode, Switcher4Node, ScreenOutputNode

class GraphContextMenu(QtGui.QMenu):
	def __init__(self, scene, newNodePos):
		super(GraphContextMenu, self).__init__()
		self.addMenu(GraphSourcesMenu(scene, newNodePos))
		self.addMenu(GraphSwitchesMenu(scene, newNodePos))
		self.addMenu(GraphDisplayMenu(scene, newNodePos))
		self.addSeparator()

		action = self.addAction("Graph")
		action.triggered.connect(scene.makeGraph)

class GraphSourcesMenu(QtGui.QMenu):
	def __init__(self, scene, newNodePos):
		super(GraphSourcesMenu, self).__init__()
		self.setTitle('Sources')
		
		action = self.addAction("Video Test Generator")
		action.triggered.connect(lambda: scene.addNodeFromMenu(VideoTestGenNode, newNodePos))
		
		action = self.addAction("V4L2 Source")
		action.triggered.connect(lambda: scene.addNodeFromMenu(V4L2SourceNode, newNodePos))

class GraphSwitchesMenu(QtGui.QMenu):
	def __init__(self, scene, newNodePos):
		super(GraphSwitchesMenu, self).__init__()
		self.setTitle('Switches')

		action = self.addAction("4 Input Video Switcher")
		action.triggered.connect(lambda: scene.addNodeFromMenu(Switcher4Node, newNodePos))

class GraphDisplayMenu(QtGui.QMenu):
	def __init__(self, scene, newNodePos):
		super(GraphDisplayMenu, self).__init__()
		self.setTitle('Outputs')

		action = self.addAction("Screen Display")
		action.triggered.connect(lambda: scene.addNodeFromMenu(ScreenOutputNode, newNodePos))

		