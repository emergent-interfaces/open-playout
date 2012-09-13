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

        pad = self.src.get_static_pad("src")
        ghost_pad = Gst.GhostPad.new("src", pad)
        self.bin.add_pad(ghost_pad)
