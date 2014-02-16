from PySide import QtGui, QtCore
from devices.video_test_gen import VideoTestGen
from devices.camera import Camera
from devices.monitor import Monitor
from devices.switcher import Switcher
from devices.dsk import Dsk

from functools import partial

class GraphContextMenu(QtGui.QMenu):
	def __init__(self, scene, newNodePos):
		super(GraphContextMenu, self).__init__()
		self.addMenu(NewNodeMenu(scene, newNodePos, "Sources", [VideoTestGen, Camera]))
		self.addMenu(NewNodeMenu(scene, newNodePos, "Switches", [Switcher, Dsk]))
		self.addMenu(NewNodeMenu(scene, newNodePos, "Outputs", [Monitor]))

		self.addSeparator()

		action = self.addAction("Graph")
		action.triggered.connect(scene.makeGraph)

class NewNodeMenu(QtGui.QMenu):
	def __init__(self, scene, newNodePos, title, deviceClasses):
		super(NewNodeMenu, self).__init__()
		self.setTitle(title)

		for deviceClass in deviceClasses:
			action = self.addAction(deviceClass.suggested_readable_name)
			action.triggered.connect(partial(scene.addNodeFromMenu, deviceClass, newNodePos))
