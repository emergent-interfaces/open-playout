import gi
import sys
import camera
import monitor
import patch
import deck

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst, GstVideo
print Gst.version_string()


class Station(object):
    def __init__(self, config):
        self.config = config
        self.devices = []
        self.patches = []
        Gst.init(None)

        self.pipeline = Gst.Pipeline()

        for device_details in self.config["devices"]:
            device = self.device_factory(device_details)
            if device:
                self.add_device(device)

        for patch_details in self.config["patches"]:
            p = self.patch_factory(patch_details)
            if p:
                self.add_patch(p)

        self.bus = self.pipeline.get_bus()
        self.bus.connect('message::eos', self.on_bus_eos)
        #self.bus.connect('sync-message::element', self.on_sync_message)
        #self.bus.connect('message', self.on_bus_message)
        self.bus.add_signal_watch()

    def device_factory(self, details):
        if details["type"] == "camera":
            return camera.Camera(details["name"])
        elif details["type"] == "monitor":
            return monitor.Monitor(details["name"],
                                   details["size"],
                                   details["location"])
        elif details["type"] == "deck":
            return deck.Deck(details["name"])

        return None

    def patch_factory(self, details):
        src_device_name, separator, src_port_name = details["src"].partition('.')
        sink_device_name, separator, sink_port_name = details["sink"].partition('.')

        src_port = self.find_device_by_name(src_device_name).get_port(src_port_name)
        sink_port = self.find_device_by_name(sink_device_name).get_port(sink_port_name)

        return patch.Patch(src_port, sink_port)

    def add_device(self, device):
        self.pipeline.add(device.get_bin())
        self.devices.append(device)

    def add_patch(self, patch):
        self.patches.append(patch)

    def find_device_by_name(self, name):
        for device in self.devices:
            if device.name == name:
                return device

        return None

    def find_all_monitors(self):
        monitors = []
        for device in self.devices:
            if isinstance(device, monitor.Monitor):
                monitors.append(device)

        return monitors

    def swap(self):
        if self.cam1.active:
            self.cam1.fall_back()
        else:
            self.cam1.stand_up()

        self.assign_drawing_area()

    def assign_drawing_area(self, drawing_area, monitor_name):
        sink = self.find_device_by_name(monitor_name).get_sink()
        sink.set_window_handle(drawing_area.get_window().get_xid())

    def on_sync_message(self, bus, message):
        structure = message.get_structure()
        print structure

    def on_bus_message(self, bus, message):
        print self.message_details(message)

    def on_bus_eos(self, bus, message):
        print "EOS Received"
        print self.message_details(message)
        self.swap()
        #self.stop()

    def message_details(self, message):
        text = "Message:"
        text += " " + message.src.name
        text += " " + str(message.type)
        return text

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)
