print "Loading Configuration"

# # Simple test
# self.graphWidget.scene.addNode(ScreenOutputNode("screen1", (320,240), (0,0)), QtCore.QPointF(300,100))
# self.graphWidget.scene.addNode(VideoTestGenNode("video1"), QtCore.QPointF(100,100))
# self.graphWidget.scene.addWire('video1.out', 'screen1.in')

# # Switcher control panel test
# self.graphWidget.scene.addNode(VideoTestGenNode("video1"), QtCore.QPointF(0,0))
# v1 = self.graphWidget.scene.addNode(VideoTestGenNode("video2"), QtCore.QPointF(0,100))
# v1.device.pattern.set_value(1)
# self.graphWidget.scene.addNode(Switcher4Node("switcher1"), QtCore.QPointF(200,0))
# self.graphWidget.scene.addNode(ScreenOutputNode("screen1", (320,240), (0,0)), QtCore.QPointF(400,0))
# self.graphWidget.scene.addNode(ScreenOutputNode("screen2", (320,240), (330,0)), QtCore.QPointF(400,100))

# self.graphWidget.scene.addWire('video1.out', 'switcher1.in1')
# self.graphWidget.scene.addWire('video2.out', 'switcher1.in2')
# self.graphWidget.scene.addWire('switcher1.prog_out', 'screen1.in')
# self.graphWidget.scene.addWire('switcher1.prev_out', 'screen2.in')

# # Overlay test
# self.graphWidget.scene.addNode(VideoTestGenNode("video1"), QtCore.QPointF(100,100))
# node = self.graphWidget.scene.addNode(DskNode("dsk1"), QtCore.QPointF(300,100))
# node.device.file.set_value('../media/lower_third.svg')
# self.graphWidget.scene.addNode(ScreenOutputNode("screen1", (320,240), (0,0)), QtCore.QPointF(500,100))
# self.graphWidget.scene.addWire('video1.out', 'dsk1.in')
# self.graphWidget.scene.addWire('dsk1.out', 'screen1.in')