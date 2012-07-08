import gi
import sys

try:
	gi.require_version('Gst','1.0')
except ValueError:
	print 'Could not find required Gstreamer library'
	sys.exit(1)
	
from gi.repository import Gst
	
class Camera(object):
	def __init__(self,name):
		self.name = name
		
		self.bin = Gst.Bin.new('camera_bin')
		self.src = Gst.ElementFactory.make('v4l2src', None)
		self.caps_filter = Gst.ElementFactory.make('capsfilter', None)
		
		self.bin.add(self.src)
		self.bin.add(self.caps_filter)
		
		self.src.link(self.caps_filter)
		
		pad = self.caps_filter.get_static_pad("src")
		ghost_pad = Gst.GhostPad.new("src",pad)
		self.bin.add_pad(ghost_pad)
		
		self.caps_filter.set_property('caps',
	  	Gst.caps_from_string("video/x-raw, width=640, height=480"))

		self.active = True

	def get_bin(self):
		return self.bin

	def get_src(self):
		return self.bin.get_static_pad('src')

	def fall_back(self):
		self.backup_source = Gst.ElementFactory.make('videotestsrc',None)
		self.bin.add(self.backup_source)

		self.src.set_state(Gst.State.NULL)

		self.src.unlink(self.caps_filter)
		del self.src
		self.backup_source.link(self.caps_filter)

		self.backup_source.set_state(Gst.State.PLAYING)

		self.active = False

	def stand_up(self):
		self.src = Gst.ElementFactory.make('v4l2src', None)
		self.bin.add(self.src)

		self.backup_source.set_state(Gst.State.NULL)

		self.backup_source.unlink(self.caps_filter)
		del self.backup_source
		self.src.link(self.caps_filter)

		self.src.set_state(Gst.State.PLAYING)

		self.active = True
