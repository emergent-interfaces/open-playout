import gi
import sys

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst

class Device(object):
    def __init__(self, name):
        self.name = name
        self.bin = Gst.Bin.new(self.name)

    # todo Implement device_pad_name choice
    def add_input_port_on(self, device, device_pad_name="sink"):
        intervideosrc = Gst.ElementFactory.make('intervideosrc', None)
        self.bin.add(intervideosrc)

        intervideosrc.link(device)

    # todo Implement device_pad_name choice
    def add_output_port_on(self, device, device_pad_name="src"):
        intervideosink = Gst.ElementFactory.make('intervideosink', None)
        self.bin.add(intervideosink)

        device.link(intervideosink)

    def get_bin(self):
        return self.bin

    def start_playing(self):
        self.bin.set_state(Gst.State.PLAYING)