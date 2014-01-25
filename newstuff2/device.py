import gi
import sys

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst

class Device(object):
    DEFAULT_VIDEO_CAPS = "video/x-raw,format=I420,width=320,height=240"

    def __init__(self, name):
        self.name = name
        self.bin = Gst.Bin.new(self.name)
        self.ports = []

    # todo Implement device_pad_name choice
    def add_input_port_on(self, device, device_pad_name="sink", port_name="in"):
        element_name = self.bin.get_name() + "." + port_name
        intervideosrc = Gst.ElementFactory.make('intervideosrc', element_name)
        self.bin.add(intervideosrc)

        channel = element_name
        intervideosrc.set_property('channel', channel)
        self.ports.append(channel)

        intervideosrc.link(device)

    # todo Implement device_pad_name choice
    def add_output_port_on(self, device, device_pad_name="src", port_name="out"):
        element_name = self.bin.get_name() + "." + port_name
        intervideosink = Gst.ElementFactory.make('intervideosink', element_name)
        self.bin.add(intervideosink)

        channel = element_name
        intervideosink.set_property('channel', channel)
        self.ports.append(channel)

        device.link(intervideosink)

    def get_bin(self):
        return self.bin

    def set_playing(self):
        self.bin.set_state(Gst.State.PLAYING)

    def set_null(self):
        self.bin.set_state(Gst.State.NULL)

    def set_ready(self):
        self.bin.set_state(Gst.State.READY)