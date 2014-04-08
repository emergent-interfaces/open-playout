import gi
import sys
from device import Device

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class Camera(Device):
    suggested_name = "camera"
    suggested_readable_name = "Camera"

    def __init__(self, name):
        Device.__init__(self, name)

        self.src = Gst.ElementFactory.make('v4l2src', None)
        self.bin.add(self.src)

        self.convert = Gst.ElementFactory.make('videoconvert', None)
        self.bin.add(self.convert)

        self.caps_filter = Gst.ElementFactory.make('capsfilter', None)
        self.caps_filter.set_property('caps', Gst.caps_from_string(Device.DEFAULT_VIDEO_CAPS))
        self.bin.add(self.caps_filter)

        self.src.link(self.convert)
        self.convert.link(self.caps_filter)

        self.add_output_video_port_on(self.caps_filter, "src")

        # pad = self.text_overlay.get_static_pad("src")
        # ghost_pad = Gst.GhostPad.new("src", pad)
        # self.bin.add_pad(ghost_pad)
        # ghost_pad.add_probe(Gst.PadProbeType.EVENT_DOWNSTREAM, self.probe_callback, None)

        # self.active = True
        # self.device = self.src.get_property('device')

    # def fall_back(self):
    #     self.backup_source = Gst.ElementFactory.make('videotestsrc', None)
    #     self.bin.add(self.backup_source)

    #     self.src.set_state(Gst.State.NULL)

    #     self.src.unlink(self.caps_filter)
    #     del self.src
    #     self.backup_source.link(self.caps_filter)

    #     overlay_text = self.name + '\n' + 'Lost source ' + self.device
    #     self.set_overlay_text(overlay_text)

    #     self.backup_source.set_state(Gst.State.PLAYING)

    #     self.active = False

    # def stand_up(self):
    #     self.src = Gst.ElementFactory.make('v4l2src', None)
    #     self.bin.add(self.src)

    #     self.backup_source.set_state(Gst.State.NULL)

    #     self.backup_source.unlink(self.caps_filter)
    #     del self.backup_source
    #     self.src.link(self.caps_filter)

    #     self.set_overlay_text('')

    #     self.src.set_state(Gst.State.PLAYING)

    #     self.active = True
    #     self.device = self.src.get_property('device')
