import gi
import sys
from device import Device

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class Monitor(Device):
    def __init__(self, name, size, location):
        Device.__init__(self, name)
        self.size = size
        self.location = location

        self.convert = Gst.ElementFactory.make('videoconvert', None)
        self.bin.add(self.convert)

        self.scale = Gst.ElementFactory.make('videoscale', None)
        self.bin.add(self.scale)

        self.sink = Gst.ElementFactory.make('xvimagesink', None)
        self.bin.add(self.sink)

        caps = Gst.caps_from_string(Device.DEFAULT_VIDEO_CAPS)
        self.convert.link_filtered(self.scale, caps)
        self.scale.link(self.sink)

        self.add_input_port_on(self.convert)

        
    def get_sink(self):
        return self.sink