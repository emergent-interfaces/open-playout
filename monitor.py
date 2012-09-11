import gi
import sys
import device

try:
	gi.require_version('Gst','1.0')
except ValueError:
	print 'Could not find required Gstreamer library'
	sys.exit(1)

from gi.repository import Gst

class Monitor(device.Device):
	def __init__(self, name, size, location):
		device.Device.__init__(self, name)
		self.size = size
		self.location = location

		self.sink = Gst.ElementFactory.make('xvimagesink', None)
		self.bin.add(self.sink)

		pad = self.sink.get_static_pad("sink")
		ghost_pad = Gst.GhostPad.new("sink",pad)
		self.bin.add_pad(ghost_pad)

	def get_sink(self):
		return self.sink