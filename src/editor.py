import sys
import PySide
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow
from graph.graph import GraphWidget

from station import Station
from display import Display
from devices.monitor import Monitor
from devices.video_test_gen import VideoTestGen
from devices.camera import Camera
from devices.switcher import Switcher
from devices.dsk import Dsk

from graph.node import Node

class GuiApp():
    def __init__(self):
        pass

    def start(self, args):
        self.station = Station({}, args)
        self.station.run()

        self.app = QApplication(sys.argv)
        frame = MainWindow(self.station)
        frame.show()
        sys.exit(self.app.exec_())

    def exit(self):
        self.app.exit()


class Communicate(QtCore.QObject):
    cmdReceived = QtCore.Signal(str)

class MainWindow(QMainWindow):
    def __init__(self, station, parent=None):
        super(MainWindow, self).__init__(parent)
        self.station = station
        self.initUI()
        execfile('config.py')

    def initUI(self):
        hbox = QtGui.QHBoxLayout(self)

        nodesFrame = QtGui.QFrame(self)
        nodesFrame.setFrameShape(QtGui.QFrame.StyledPanel)

        consoleFrame = QtGui.QFrame(self)
        consoleFrame.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(nodesFrame)
        splitter.addWidget(consoleFrame)

        hbox.addWidget(splitter)
        self.setLayout(hbox)

        # Console input
        hbox2 = QtGui.QHBoxLayout()
        consoleInput = QtGui.QLineEdit()
        self.consoleInput = consoleInput
        hbox2.addWidget(consoleInput)
        consoleFrame.setLayout(hbox2)
        consoleInput.returnPressed.connect(self.doConsoleCmd)

        # Add graph
        self.graphWidget = GraphWidget()
        hbox3 = QtGui.QHBoxLayout()
        nodesFrame.setLayout(hbox3)
        hbox3.addWidget(self.graphWidget)

        self.setCentralWidget(splitter)
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('QtGui.QSplitter')

        # Connect GraphWidget
        self.graphWidget.nodeAdded.connect(self.addDeviceForNode)
        self.graphWidget.nodeRemoved.connect(self.removeDeviceForNode)
        self.graphWidget.wireAdded.connect(self.addLinkForWire)
        self.graphWidget.wireRemoved.connect(self.removeLinkForWire)
        self.graphWidget.requestGraphDebug.connect(self.makeGraphDebug)
        self.graphWidget.controlPanelRequested.connect(self.makeControlPanel)

    def install(self, deviceClass, name, (x,y)):
        node = self.graphWidget.scene.addNode(Node(name, deviceClass), QtCore.QPointF(x,y))
        return node.device, node

    def wire(self, channel1, channel2):
        self.graphWidget.scene.addWire(channel1, channel2)

    def addDeviceForNode(self, node):
        if node.deviceClass == Monitor:
            device = Monitor(node.name, (320, 240), (0, 0))
            device.display = Display(self, device)

        if node.deviceClass == VideoTestGen:
            device = VideoTestGen(node.name)

        if node.deviceClass == Camera:
            device = Camera(node.name)

        if node.deviceClass == Switcher:
            device = Switcher(node.name, 4)

        if node.deviceClass == Dsk:
            device = Dsk(node.name)

        self.station.add_device(device)
        node.setDevice(device)

    def removeDeviceForNode(self, node):
        device = self.station.find_device_by_name(node.name)
        self.station.remove_device(device)

    def addLinkForWire(self, wire):
        port1_name = wire.port1.fullName()
        port2_name = wire.port2.fullName()
        self.station.link("-".join([port1_name, port2_name]), port1_name, port2_name)

    def removeLinkForWire(self, wire):
        self.station.unlink(wire.port1.fullName(), wire.port2.fullName())

    def doConsoleCmd(self):
        cmd = self.consoleInput.text()
        sig = Communicate()
        sig.cmdReceived.emit(cmd)

        self.consoleInput.clear()

    def makeGraphDebug(self):
        self.station.graph_pipeline()

    def makeControlPanel(self, node):
        controlPanel = node.device.make_control_panel(self)
        controlPanel.show()
        controlPanel.center_at(QtGui.QCursor.pos())

    def closeEvent(self, event):
        for monitor in self.station.find_devices_by_type(Monitor):
            monitor.set_window_id(0)   

if __name__ == "__main__":
        editor = Editor()
        sys.exit(editor.start())


