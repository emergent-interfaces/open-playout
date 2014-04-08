from PySide import QtGui, QtCore
from port import Port
from wire import Wire

class Node(QtGui.QGraphicsItem):
    NodeTopPadding = 40
    NodeBottomPadding = 20

    def __init__(self, name, deviceClass):
        super(Node, self).__init__()
        self.name = name
        self.deviceClass = deviceClass
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

        self.ports = []

        self.brushes = {}
        self.brushes['background'] = QtGui.QBrush(QtGui.QColor(107,107,107), QtCore.Qt.SolidPattern)
        self.colors = {}
        self.colors['normalBorder'] = QtGui.QColor(0,0,0)
        self.colors['selectedBorder'] = QtGui.QColor(200, 120, 10)

        self.sizeBackground()

        self.device = None

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange and self.scene():
            for wire in self.wires():
                wire.prepareGeometryChange()
            self.scene().update()

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def setDevice(self, device):
        self.device = device
        for port in device.ports:
            self.createPort(port['name'], port['media_type'], port['direction'])

    def createPort(self, name, media_type, direction='in'):
        port = Port(name, media_type, direction)
        self.ports.append(port)
        self.prepareGeometryChange()
        port.setParentItem(self)
        self.arrangePorts()
        self.sizeBackground()

    def inPorts(self):
        return [p for p in self.ports if p.direction=='in']

    def outPorts(self):
        return [p for p in self.ports if p.direction=='out']
    
    def arrangePorts(self):
        for i, port in enumerate(self.inPorts()):
            port.setPos(0, Port.PortHeight * i + self.NodeTopPadding)

        for i, port in enumerate(self.outPorts()):
            port.setPos(150, Port.PortHeight * i + self.NodeTopPadding)

    def sizeBackground(self):
        numPortsTall = max(len(self.inPorts()), len(self.outPorts()))

        self.backgroundHeight = (self.NodeTopPadding + 
            self.NodeBottomPadding + 
            (numPortsTall-1)*Port.PortHeight)

    def boundingRect(self):
        penWidth = 1.0
        return QtCore.QRectF(- penWidth / 2,- penWidth / 2,
                      150 + penWidth, self.backgroundHeight)

    def paint(self, painter, option, widget):
        painter.setBrush(self.brushes['background'])

        if self.isSelected():
            painter.setPen(self.colors['selectedBorder'])
            painter.drawRoundedRect(0, 0, 150, self.backgroundHeight, 5, 5)
        else:
            painter.setPen(self.colors['normalBorder'])
            painter.drawRoundedRect(0, 0, 150, self.backgroundHeight, 5, 5)

        painter.setPen(self.colors['normalBorder'])
        painter.drawText(QtCore.QRectF(0, 0, 150, 20), QtCore.Qt.AlignCenter, self.name)

    def delete(self):
        for wire in self.wires():
            wire.delete()

        self.scene().notifyView('remove', self)
        self.scene().removeItem(self)

    def wires(self):
        wires = [item for item in self.scene().items()
            if type(item)==Wire
            if (self.hasPort(item.port1) or self.hasPort(item.port2))]

        return wires

    def hasPort(self, port):
        if port in self.childItems():
            return True
        else:
            return False

    def mouseDoubleClickEvent(self, event):
        self.scene().notifyView('show', self)