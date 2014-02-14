import gi
import sys
from device import Device
from observable_variable import ObservableVariable
from monitor_control_panel import MonitorControlPanel

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class Monitor(Device):
    def __init__(self, name, size, location):
        Device.__init__(self, name)
        self.ControlPanelClass = MonitorControlPanel

        self.size = ObservableVariable(size)
        self.size.changed.connect(self.change_size)
        self.location = ObservableVariable(location)
        self.location.changed.connect(self.change_location)

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

    def set_window_id(self, id):
        self.get_sink().set_window_handle(id)

    def change_size(self):
        self.display.set_size(*self.size.get_value())

    def change_location(self):
        self.display.set_location(*self.location.get_value())