import gi
import sys
import camera

try:
	gi.require_version('Gst','1.0')
except ValueError:
	print 'Could not find required Gstreamer library'
	sys.exit(1)

from gi.repository import Gst, GstVideo
print Gst.version_string()

class Station(object):
	def __init__(self):
		Gst.init(None)
				
		self.pipeline = Gst.Pipeline()
		self.cam1 = camera.Camera('cam1')
		self.add_equipment(self.cam1)
		
		self.sink = Gst.ElementFactory.make('xvimagesink', None)
		self.pipeline.add(self.sink)
		
		self.cam1.get_bin().link(self.sink)

		self.bus = self.pipeline.get_bus()
		self.bus.connect('message::eos', self.on_bus_eos)
		self.bus.connect('sync-message::element', self.on_sync_message)
		self.bus.connect('message', self.on_bus_message)
		self.bus.add_signal_watch()
	
	def add_equipment(self, equipment):
		self.pipeline.add(self.cam1.get_bin())
		
	def swap(self):
		if self.cam1.active:
			self.cam1.fall_back()
		else:
			self.cam1.stand_up()

		self.assign_drawing_area()
		
	def assign_drawing_area(self, drawing_area=None):
		if drawing_area:
			self.drawing_area = drawing_area
		
		self.sink.set_window_handle(self.drawing_area.get_window().get_xid())	

	def on_sync_message(self, bus, message):
		structure = message.get_structure()
		print structure

	def on_bus_message(self, bus, message):
		pass
		
	def on_bus_eos(self, bus, message):
		print "EOS Received"
		print message
		self.stop()
	
	def run(self):
		self.pipeline.set_state(Gst.State.PLAYING)
		
	def stop(self):
		self.pipeline.set_state(Gst.State.NULL)
