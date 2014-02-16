import gi
import sys
from device import Device
from observable_variable import ObservableVariable

from video_test_gen_control_panel import VideoTestGenControlPanel

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class VideoTestGen(Device):
    suggested_name = "videotestgen"
    suggested_readable_name = "Video Test Generator"

    def __init__(self, name, pattern=0):
        Device.__init__(self, name)
        self.ControlPanelClass = VideoTestGenControlPanel

        self.pattern = ObservableVariable(pattern)
        self.pattern.changed.connect(self.change_pattern)

        self.src = Gst.ElementFactory.make('videotestsrc', None)
        self.bin.add(self.src)
        self.src.set_property('pattern', self.pattern.get_value())

        self.convert = Gst.ElementFactory.make('videoconvert', None)
        self.bin.add(self.convert)

        self.text_overlay = Gst.ElementFactory.make('textoverlay', None)
        self.bin.add(self.text_overlay)
        self.text_overlay.set_property("text", self.name)
        self.text_overlay.set_property("shaded-background", True)

        self.caps_filter = Gst.ElementFactory.make('capsfilter', None)
        self.bin.add(self.caps_filter)

        caps = Gst.caps_from_string(Device.DEFAULT_VIDEO_CAPS)
        self.caps_filter.set_property('caps', caps)

        self.src.link(self.text_overlay)
        self.text_overlay.link(self.convert)
        self.convert.link(self.caps_filter)

        self.add_output_port_on(self.caps_filter, "src")

    def change_pattern(self):
        self.src.set_property('pattern', self.pattern.get_value())
