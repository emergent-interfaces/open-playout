from PySide import QtGui, QtCore
from wire import Wire


class Port(QtGui.QGraphicsItem):
    PortHeight = 20

    def __init__(self, name, media_type, direction='in'):
        super(Port, self).__init__()
        self.setAcceptHoverEvents(True)
        self.hovered = False
        self.media_type = media_type

        self.direction = direction
        self.name = name

        self.brushes = {}

        if self.media_type == "video":
            self.brushes['bkg'] = QtGui.QBrush(QtGui.QColor(157, 157, 157),
                                               QtCore.Qt.SolidPattern)
            self.brushes['bkgHover'] = QtGui.QBrush(QtGui.QColor(200, 120, 10),
                                                    QtCore.Qt.SolidPattern)
        elif self.media_type == "audio":
            self.brushes['bkg'] = QtGui.QBrush(QtGui.QColor(157, 157, 200),
                                               QtCore.Qt.SolidPattern)
            self.brushes['bkgHover'] = QtGui.QBrush(QtGui.QColor(157, 157, 255),
                                                    QtCore.Qt.SolidPattern)

    def fullName(self):
        return self.parentItem().name + "." + self.name

    def boundingRect(self):
        penWidth = 1.0

        fm = QtGui.QFontMetrics(QtGui.QFont())
        nameWidth = fm.width(self.name)
        nameHeight = fm.height()

        if self.direction == "in":
            self.bounds = QtCore.QRectF(-5 - penWidth / 2, -nameHeight/2,
                                        15 + nameWidth, nameHeight)
        else:
            self.bounds = QtCore.QRectF(-10 - nameWidth - penWidth / 2, -nameHeight/2,
                                        15 + nameWidth, nameHeight)

        return self.bounds

    def paint(self, painter, option, widget):
        #painter.drawRect(self.bounds)

        fm = painter.fontMetrics()
        nameWidth = fm.width(self.name)
        nameHeight = fm.height()

        if self.hovered:
            painter.setBrush(self.brushes['bkgHover'])
        else:
            painter.setBrush(self.brushes['bkg'])
        #painter.drawEllipse(0,0,1,1)
        painter.drawEllipse(-5, -5, 10, 10)

        if self.direction == "in":
            painter.drawText(10, nameHeight/2 - 2, self.name)
        else:
            painter.drawText(-10 - nameWidth, nameHeight/2 - 2, self.name)
        #painter.drawEllipse(10, nameHeight/2,1,1)
        #painter.drawEllipse(10, -nameHeight/2,1,1)

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        scene = self.scene()
        wire = Wire(self)
        scene.addItem(wire)

        self.temporaryWire = wire

    def mouseReleaseEvent(self, event):
        endPort = self.portAt(event.scenePos())

        if endPort:
            self.temporaryWire.setPort2(endPort)
            if not self.temporaryWire.isValid():
                self.scene().removeItem(self.temporaryWire)
                del self.temporaryWire
            else:
                self.scene().notifyView('add', self.temporaryWire)
                del self.temporaryWire

        else:
            self.scene().removeItem(self.temporaryWire)
            del self.temporaryWire

        self.temporaryWire = None
        self.scene().update()

    def mouseMoveEvent(self, event):
        if self.temporaryWire:
            self.temporaryWire.setTemporaryEndpoint(event.scenePos())

        self.scene().update()

    def portAt(self, position):
        items = [item for item in self.scene().items(position) if type(item) == Port]
        return items[0] if items else None
