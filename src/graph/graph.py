import PySide
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow
from PySide.QtCore import QPointF

from node import Node
from wire import Wire
from port import Port
from node_types import VideoTestGenNode, V4L2SourceNode, Switcher4Node, ScreenOutputNode
from graph_context_menu import GraphContextMenu

# =================================================================
# TODO THIS SHOULD SEND SIGNALS WHEN ADDING, LINKING, AND DELETEING
# =================================================================
class GraphWidget(QtGui.QGraphicsView):
    nodeAdded = QtCore.Signal(Node)
    nodeRemoved = QtCore.Signal(Node)
    wireAdded = QtCore.Signal(Wire)
    wireRemoved = QtCore.Signal(Wire)
    requestGraphDebug = QtCore.Signal()
    controlPanelRequested = QtCore.Signal(Node)

    def __init__(self):
        self.scene = PlayoutGraphicsScene(self)
        self.scene.notifyView = self.notifyView

        super(GraphWidget, self).__init__(self.scene)
        self.initUI()

    def initUI(self):
        #self.setSceneRect(self.rect())

        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.setInteractive(True)
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

        self.brushes = {}
        self.brushes['background'] = QtGui.QBrush(QtGui.QColor(57,57,57), QtCore.Qt.SolidPattern)
        self.setBackgroundBrush(self.brushes['background'])

    # def resizeEvent(self, event):
    #     self.setSceneRect(self.rect())

    def wheelEvent(self, event):
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        scaleFactor = 1.15
        if event.delta() > 0:
            self.scale(scaleFactor, scaleFactor)
        else:
            self.scale(1.0/scaleFactor, 1.0/scaleFactor)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            items = self.scene.selectedItems()
            for item in items:
                item.delete()                                  

    # Generic function available on QGraphicsScene to perform signal emits from
    # the QGraphicsView
    def notifyView(self, action, object):
        if action == "add":
            if isinstance(object, Node):
                self.nodeAdded.emit(object)
            if isinstance(object, Wire):
                self.wireAdded.emit(object)

        if action == "remove":
            if isinstance(object, Node):
                self.nodeRemoved.emit(object)
            if isinstance(object, Wire):
                self.wireRemoved.emit(object)

        if action == "show":
            if isinstance(object, Node):
                self.controlPanelRequested.emit(object)

class PlayoutGraphicsScene(QtGui.QGraphicsScene):
    def __init__(self, view):
        super(PlayoutGraphicsScene, self).__init__()
        self.view = view

    def contextMenuEvent(self, event):
        menu = GraphContextMenu(self, event.scenePos())
        menu.exec_(event.screenPos())

    def makeGraph(self):
        self.view.requestGraphDebug.emit()

    def addNodeFromMenu(self, nodeClass, position):
        if nodeClass == ScreenOutputNode:
            name, ok = QtGui.QInputDialog.getText(self.view, "Create Screen Display",
                "Name:", text=self.freeName("display"))

            if ok:
                self.addNode(ScreenOutputNode(name), position)

        if nodeClass == Switcher4Node:
            name, ok = QtGui.QInputDialog.getText(self.view, "Create 4-Input Switcher",
                "Name:", text=self.freeName("switcher"))

            if ok:    
                self.addNode(Switcher4Node(name), position)

        if nodeClass == VideoTestGenNode:
            name, ok = QtGui.QInputDialog.getText(self.view, "Create Video Test Generator",
                "Name:", text=self.freeName("videotestgen"))

            if ok:  
                self.addNode(VideoTestGenNode(name), position)

        if nodeClass == V4L2SourceNode:
            name, ok = QtGui.QInputDialog.getText(self.view, "Create V4L2 Source",
                "Name:", text=self.freeName("v4l2source"))

            if ok:
                self.addNode(V4L2SourceNode(name), position) 

    def addNode(self, node, position=QPointF(0,0)):
        node.setPos(position)
        self.addItem(node)
        self.view.notifyView('add', node)

    def addWire(self, portFullName1, portFullName2):
        port1 = self.portByFullName(portFullName1)
        port2 = self.portByFullName(portFullName2)

        wire = Wire(port1, port2)
        self.addItem(wire)
        self.view.notifyView('add', wire)

    def ports(self):
        return [item for item in self.items() if isinstance(item, Port)]

    def portByFullName(self, fullName):
        return next(port for port in self.ports() if port.fullName() == fullName)

    def freeName(self, name):
        node_names = [item.name for item in self.items() if isinstance(item, Node)]
        n = 1

        while (name + str(n)) in node_names:
            n = n+1

        return name + str(n)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    testWidget = GraphWidget()
    testWidget.show()
    testWidget.setGeometry(300, 300, 600, 600)
    sys.exit(app.exec_())