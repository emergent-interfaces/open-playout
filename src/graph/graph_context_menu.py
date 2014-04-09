from PySide import QtGui
from devices.video_test_gen import VideoTestGen
from devices.camera import Camera
from devices.monitor import Monitor
from devices.switcher import Switcher
from devices.dsk import Dsk
from devices.ustream_provider import UstreamProvider
from devices.audio_test_gen import AudioTestGen
from devices.audio_out import AudioOut

from functools import partial


class GraphContextMenu(QtGui.QMenu):
    def __init__(self, scene, newNodePos):
        super(GraphContextMenu, self).__init__()
        sources = [VideoTestGen, Camera, AudioTestGen]
        switches = [Switcher, Dsk]
        outputs = [Monitor, UstreamProvider, AudioOut]

        self.addMenu(NewNodeMenu(scene, newNodePos, "Sources", sources))
        self.addMenu(NewNodeMenu(scene, newNodePos, "Switches", switches))
        self.addMenu(NewNodeMenu(scene, newNodePos, "Outputs", outputs))

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
