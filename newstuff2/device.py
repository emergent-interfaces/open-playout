import gi
import sys
import uuid

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
        self.ports = {}

    # todo Implement device_pad_name choice
    def add_input_port_on(self, device, device_pad_name="sink", port_name="in"):
        intervideosrc = Gst.ElementFactory.make('intervideosrc', None)
        self.bin.add(intervideosrc)

        channel_uuid = 'b'#uuid.uuid1()
        intervideosrc.set_property('channel', channel_uuid)
        self.ports[port_name] = intervideosrc

        intervideosrc.link(device)

    # todo Implement device_pad_name choice
    def add_output_port_on(self, device, device_pad_name="src", port_name="out"):
        intervideosink = Gst.ElementFactory.make('intervideosink', None)
        self.bin.add(intervideosink)

        channel_uuid = 'a'#uuid.uuid1()
        intervideosink.set_property('channel', channel_uuid)
        self.ports[port_name] = intervideosink

        device.link(intervideosink)

    def get_port_from_uuid(uuid):
        pass


    def get_bin(self):
        return self.bin

    def set_playing(self):
        self.bin.set_state(Gst.State.PLAYING)

    def set_null(self):
        self.bin.set_state(Gst.State.NULL)

    def set_ready(self):
        self.bin.set_state(Gst.State.READY)