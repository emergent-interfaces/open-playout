import gi
import sys
from device import Device

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class VideoTestGen(Device):
    def __init__(self, name, pattern=0):
        Device.__init__(self, name)

        self.src = Gst.ElementFactory.make('videotestsrc', None)
        self.src.set_property('pattern', pattern)
        self.bin.add(self.src)

        self.text_overlay = Gst.ElementFactory.make('textoverlay', None)
        self.bin.add(self.text_overlay)
        self.text_overlay.set_property("text", self.name)
        self.text_overlay.set_property("shaded-background", True)

        self.src.link(self.text_overlay)
        pad = self.text_overlay.get_static_pad("src")
        ghost_pad = Gst.GhostPad.new("src", pad)
        self.bin.add_pad(ghost_pad)
