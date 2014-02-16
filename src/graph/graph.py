import PySide
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow
from PySide.QtCore import QPointF

from node import Node
from wire import Wire
from port import Port
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

    def addNodeFromMenu(self, deviceClass, position):
        name, ok = QtGui.QInputDialog.getText(
            self.view,
            "Create " + deviceClass.suggested_readable_name,
            "Name:",
            text=self.freeName(deviceClass.suggested_name)
        )

        if ok:
            self.addNode(Node(name, deviceClass), position)

    def addNode(self, node, position=QPointF(0,0)):
        node.setPos(position)
        self.addItem(node)
        self.view.notifyView('add', node)
        
        return node

    def addWire(self, portFullName1, portFullName2):
        port1 = self.portByFullName(portFullName1)
        port2 = self.portByFullName(portFullName2)

        wire = Wire(port1, port2)
        self.addItem(wire)
        self.view.notifyView('add', wire)

        return wire

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