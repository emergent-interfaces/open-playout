import gi
import sys
from device import Device

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class Link(Device):
    def __init__(self, name, channel1, channel2):
        Device.__init__(self, name)

        intervideosrc = Gst.ElementFactory.make('intervideosrc', None)
        self.port_1 = channel1
        intervideosrc.set_property('channel', channel1)
        self.bin.add(intervideosrc)

        intervideosink = Gst.ElementFactory.make('intervideosink', None)
        self.port_2 = channel2
        intervideosink.set_property('channel', channel2)
        self.bin.add(intervideosink)

        intervideosrc.link(intervideosink)