from node import Node

class VideoTestGenNode(Node):
	def __init__(self, name):
		super(VideoTestGenNode, self).__init__(name)
		self.createPort('out', 'out')

class V4L2SourceNode(Node):
	def __init__(self, name):
		super(V4L2SourceNode, self).__init__(name)
		self.createPort('out', 'out')

class Switcher4Node(Node):
	def __init__(self, name):
		super(Switcher4Node, self).__init__(name)
		self.createPort('in1')
		self.createPort('in2')
		self.createPort('in3')
		self.createPort('in4')
		self.createPort('prog_out', 'out')
		self.createPort('prev_out', 'out')

class ScreenOutputNode(Node):
	def __init__(self, name):
		super(ScreenOutputNode, self).__init__(name)
		self.createPort('in')