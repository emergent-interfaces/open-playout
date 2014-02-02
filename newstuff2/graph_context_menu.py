from PySide import QtGui, QtCore
from node_types import VideoTestGenNode, V4L2SourceNode, Switcher4Node, ScreenOutputNode

class GraphContextMenu(QtGui.QMenu):
	def __init__(self, graph, newNodePos):
		super(GraphContextMenu, self).__init__()
		self.addMenu(GraphSourcesMenu(graph, newNodePos))
		self.addMenu(GraphSwitchesMenu(graph, newNodePos))
		self.addMenu(GraphDisplayMenu(graph, newNodePos))
		self.addSeparator()
		self.addAction("Graph")

class GraphSourcesMenu(QtGui.QMenu):
	def __init__(self, graph, newNodePos):
		super(GraphSourcesMenu, self).__init__(graph, newNodePos)
		self.setTitle('Sources')
		
		action = self.addAction("Video Test Generator")
		action.triggered.connect(lambda: graph.addNodeFromMenu(VideoTestGenNode, newNodePos))
		
		action = self.addAction("V4L2 Source")
		action.triggered.connect(lambda: graph.addNodeFromMenu(V4L2SourceNode, newNodePos))

class GraphSwitchesMenu(QtGui.QMenu):
	def __init__(self, graph, newNodePos):
		super(GraphSwitchesMenu, self).__init__(graph, newNodePos)
		self.setTitle('Switches')

		action = self.addAction("4 Input Video Switcher")
		action.triggered.connect(lambda: graph.addNodeFromMenu(Switcher4Node, newNodePos))

class GraphDisplayMenu(QtGui.QMenu):
	def __init__(self, graph, newNodePos):
		super(GraphDisplayMenu, self).__init__(graph, newNodePos)
		self.setTitle('Outputs')

		action = self.addAction("Screen Display")
		action.triggered.connect(lambda: graph.addNodeFromMenu(ScreenOutputNode, newNodePos))

		