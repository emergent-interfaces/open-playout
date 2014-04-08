import gi
import sys
from device import Device

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class AudioOut(Device):
    suggested_name = "audioout"
    suggested_readable_name = "Audio Out"

    def __init__(self, name):
        Device.__init__(self, name)

        self.queue = Gst.ElementFactory.make('queue', None)
        self.queue.set_property('max-size-time', 1000000)
        self.bin.add(self.queue)

        self.sink = Gst.ElementFactory.make('alsasink', None)
        self.bin.add(self.sink)

        self.add_input_audio_port_on(self.queue)
        self.queue.link(self.sink)
