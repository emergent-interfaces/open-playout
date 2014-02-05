print "Loading Configuration"

self.graphWidget.addNode(ScreenOutputNode("screen1"), QtCore.QPointF(300,100))
self.graphWidget.addNode(VideoTestGenNode("video1"), QtCore.QPointF(100,100))