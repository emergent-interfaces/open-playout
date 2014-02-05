print "Loading Configuration"

self.graphWidget.scene.addNode(ScreenOutputNode("screen1"), QtCore.QPointF(300,100))
self.graphWidget.scene.addNode(VideoTestGenNode("video1"), QtCore.QPointF(100,100))
self.graphWidget.scene.addWire('video1.out', 'screen1.in')