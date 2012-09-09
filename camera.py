import gi
import sys
import device

try:
	gi.require_version('Gst','1.0')
except ValueError:
	print 'Could not find required Gstreamer library'
	sys.exit(1)
	
from gi.repository import Gst
	
class Camera(device.Device):
	def __init__(self,name):
		device.Device.__init__(self, name)

		self.src = Gst.ElementFactory.make('v4l2src', None)
		self.caps_filter = Gst.ElementFactory.make('capsfilter', None)
		self.text_overlay = Gst.ElementFactory.make('textoverlay', None)
		
		self.bin.add(self.src)
		self.bin.add(self.caps_filter)
		self.bin.add(self.text_overlay)

		self.configure_textoverlay()
		
		self.src.link(self.caps_filter)
		self.caps_filter.link(self.text_overlay)
		
		pad = self.text_overlay.get_static_pad("src")
		ghost_pad = Gst.GhostPad.new("src",pad)
		self.bin.add_pad(ghost_pad)
		ghost_pad.add_probe(Gst.PadProbeType.EVENT_DOWNSTREAM, self.probe_callback, None)
		
		self.caps_filter.set_property('caps',
	  	Gst.caps_from_string("video/x-raw, width=640, height=480"))

		self.active = True
		self.device = self.src.get_property('device')

	def probe_callback(self, pad, info, user_data):
		print "In probe callback "
		return Gst.PadProbeReturn.PASS
	
	def configure_textoverlay(self):
		self.text_overlay.set_property("shaded-background", True)

	def set_overlay_text(self,text):
		self.text_overlay.set_property("text",text)

	def fall_back(self):
		self.backup_source = Gst.ElementFactory.make('videotestsrc',None)
		self.bin.add(self.backup_source)

		self.src.set_state(Gst.State.NULL)

		self.src.unlink(self.caps_filter)
		del self.src
		self.backup_source.link(self.caps_filter)

		overlay_text = self.name + '\n' + 'Lost source ' + self.device
		self.set_overlay_text(overlay_text)

		self.backup_source.set_state(Gst.State.PLAYING)

		self.active = False

	def stand_up(self):
		self.src = Gst.ElementFactory.make('v4l2src', None)
		self.bin.add(self.src)

		self.backup_source.set_state(Gst.State.NULL)

		self.backup_source.unlink(self.caps_filter)
		del self.backup_source
		self.src.link(self.caps_filter)

		self.set_overlay_text('')

		self.src.set_state(Gst.State.PLAYING)

		self.active = True
		self.device = self.src.get_property('device')

