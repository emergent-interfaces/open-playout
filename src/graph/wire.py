from PySide import QtGui, QtCore

class Wire(QtGui.QGraphicsItem):
    def __init__(self, port1, port2=None):
        super(Wire, self).__init__()
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

        self.port1 = port1
        self.port2 = port2

        if self.port2:
            self.linked = True
        else:
            self.linked = False
            self.setTemporaryEndpoint(self.port1.scenePos())

        self.setZValue(-1)

        wireBrush = QtGui.QBrush(QtGui.QColor(157,157,157), QtCore.Qt.SolidPattern)
        wireSelected = QtGui.QBrush(QtGui.QColor(200,120,10), QtCore.Qt.SolidPattern)
        wireSheath = QtGui.QBrush(QtGui.QColor(0,0,0), QtCore.Qt.SolidPattern)

        self.pens = {}
        self.pens['wire'] = QtGui.QPen(wireBrush, 3)
        self.pens['wireSelected'] = QtGui.QPen(wireSelected, 3)
        self.pens['wireSheath'] = QtGui.QPen(wireSheath, 5)

    def isValid(self):
        if self.port1 == self.port2:
            return False

        if self.port1.direction == self.port2.direction:
            return False

        return True

    def setPort2(self, port2):
        self.port2 = port2
        self.linked = True
        self.prepareGeometryChange()
        self.update()

    def setTemporaryEndpoint(self, temporaryEndpoint):
        self.temporaryEndpoint = temporaryEndpoint
        self.prepareGeometryChange()
        self.update()

    def boundingRect(self):
        self.bounds = self.path().boundingRect()
        expand_qrect(self.bounds, 5)
        return self.bounds

    def shape(self):
        stroker = QtGui.QPainterPathStroker()
        wirePath = self.path()
        stroker.setWidth(20)
        return stroker.createStroke(wirePath)

    def paint(self, painter, option, widget):
        #painter.drawRect(self.bounds)

        painter.setPen(self.pens['wireSheath'])
        painter.drawPath(self.path())        

        if self.isSelected():
            painter.setPen(self.pens['wireSelected'])
        else:
            painter.setPen(self.pens['wire'])

        painter.drawPath(self.path())

    def path(self):
        # determine the QPainterPath for this wire and use this for painting
        # and bounds calculation        
        wirePath = QtGui.QPainterPath()

        if self.linked:
            x1, y1 = self.port1.scenePos().toTuple()
            x2, y2 = self.port2.scenePos().toTuple()
        else:
            x1, y1 = self.port1.scenePos().toTuple()
            x2, y2 = self.temporaryEndpoint.toTuple()

        wirePath.moveTo(x1, y1)

        if self.port1.direction == "out":
            c1 = QtCore.QPoint(x1+abs(x2-x1)*0.50, y1)
            c2 = QtCore.QPoint(x2-abs(x2-x1)*0.50, y2)
        else:
            c1 = QtCore.QPoint(x1-abs(x2-x1)*0.50, y1)
            c2 = QtCore.QPoint(x2+abs(x2-x1)*0.50, y2)
        
        end = QtCore.QPoint(x2, y2)

        wirePath.cubicTo(c1, c2, end)


        return wirePath

    def delete(self):
        self.scene().notifyView('remove', self)
        self.scene().removeItem(self)

def expand_qrect(qrect, amount):
    qrect.adjust(-amount, -amount, amount, amount)