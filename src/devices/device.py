import gi
import sys

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class Device(object):
    DEFAULT_VIDEO_WIDTH = 640
    DEFAULT_VIDEO_HEIGHT = 480
    DEFAULT_VIDEO_CAPS = "video/x-raw,format=I420,width=" + \
                         str(DEFAULT_VIDEO_WIDTH) + \
                         ",height=" + \
                         str(DEFAULT_VIDEO_HEIGHT) + \
                         ",framerate=30/1"

    DEFAULT_AUDIO_CHANNELS = 2
    DEFAULT_AUDIO_CAPS = "audio/x-raw,channels=(int)" + \
                         str(DEFAULT_AUDIO_CHANNELS) + \
                         ",rate=(int)48000"

    SINGLE_CHANNEL_AUDIO_CAPS = "audio/x-raw,channels=(int)1" + \
                                ",rate=(int)48000"

    suggested_name = "device"
    suggested_readable_name = "Device"

    def __init__(self, name):
        self.name = name
        self.bin = Gst.Bin.new(self.name)
        self.ports = []
        self.actions = {}
        self.controlPanels = []

    def add_element(self, element_name):
        element = Gst.ElementFactory.make(element_name, None)
        self.bin.add(element)
        return element

    def link_series(self, *elements):
        for i, element in enumerate(elements):
            if i == len(elements) - 1:
                break

            element.link(elements[i+1])


    # todo Implement device_pad_name choice
    def add_input_video_port_on(self, device, device_pad_name="sink", port_name="in"):
        element_name = self.bin.get_name() + "." + port_name
        intervideosrc = Gst.ElementFactory.make('intervideosrc', element_name)
        self.bin.add(intervideosrc)

        channel = element_name
        intervideosrc.set_property('channel', channel)
        self.register_port(channel, port_name, 'video', 'in')

        intervideosrc.link_filtered(device, Gst.caps_from_string(self.DEFAULT_VIDEO_CAPS))

    # todo Implement device_pad_name choice
    def add_output_video_port_on(self, device, device_pad_name="src", port_name="out"):
        element_name = self.bin.get_name() + "." + port_name
        intervideosink = Gst.ElementFactory.make('intervideosink', element_name)
        self.bin.add(intervideosink)

        channel = element_name
        intervideosink.set_property('channel', channel)
        self.register_port(channel, port_name, 'video', 'out')

        device.link_filtered(intervideosink, Gst.caps_from_string(self.DEFAULT_VIDEO_CAPS))

    # todo Implement device_pad_name choice
    def add_input_audio_port_on(self, device, device_pad_name="sink", port_name="in"):
        element_name = self.bin.get_name() + "." + port_name
        interaudiosrc = Gst.ElementFactory.make('interaudiosrc', element_name)
        self.bin.add(interaudiosrc)

        channel = element_name
        interaudiosrc.set_property('channel', channel)
        self.register_port(channel, port_name, 'audio', 'in')

        interaudiosrc.link_filtered(device, Gst.caps_from_string(self.DEFAULT_AUDIO_CAPS))

    # todo Implement device_pad_name choice
    def add_output_audio_port_on(self, device, device_pad_name="src", port_name="out"):
        element_name = self.bin.get_name() + "." + port_name
        interaudiosink = Gst.ElementFactory.make('interaudiosink', element_name)
        self.bin.add(interaudiosink)

        channel = element_name
        interaudiosink.set_property('channel', channel)
        self.register_port(channel, port_name, 'audio', 'out')

        device.link_filtered(interaudiosink, Gst.caps_from_string(self.DEFAULT_AUDIO_CAPS))

    def register_port(self, channel, name, media_type, direction):
        self.ports.append({
            'channel': channel,
            'name': name,
            'media_type': media_type,
            'direction': direction
        })

    def input_ports(self):
        return [port for port in self.ports if port[1] == 'in']

    def output_ports(self):
        return [port for port in self.ports if port[1] == 'out']

    def get_bin(self):
        return self.bin

    def prepare_for_removal(self):
        self.set_null()

    def set_playing(self):
        self.bin.set_state(Gst.State.PLAYING)

    def set_null(self):
        self.bin.set_state(Gst.State.NULL)

    def set_ready(self):
        self.bin.set_state(Gst.State.READY)

    def add_action(self, action, function_ptr, description):
        self.actions[action] = {"function": function_ptr,
                                "description": description}

    def do_action(self, action, args=None):
        if self.has_action(action):
            self.actions[action]["function"](*args)

    def has_action(self, action):
        if action in self.actions:
            return True
        else:
            return False

    def make_control_panel(self, parent):
        panel = self.ControlPanelClass(self, parent)
        self.controlPanels.append(panel)
        return panel

    def remove_control_panel(self, control_panel):
        self.controlPanels.remove(control_panel)
