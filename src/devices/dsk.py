# Requires librsvg2-dev, python-cairo
import gi
import sys
import cairo
from device import Device
from observable_variable import ObservableVariable
from control_panels.dsk_control_panel import DskControlPanel
import time

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class Dsk(Device):
    suggested_name = "dsk"
    suggested_readable_name = "DSK"

    def __init__(self, name):
        Device.__init__(self, name)
        self.ControlPanelClass = DskControlPanel

        self.file = ObservableVariable()
        self.file.changed.connect(self.file_changed)

        self.alpha = ObservableVariable(0)
        self.alpha.changed.connect(self.alpha_changed)

        # While input convert doesn't seem explicitly necessary, it seems to
        # give better performance.  Not sure why.
        self.inputconvert = self.add_element('videoconvert')
        self.mixer = self.add_element('videomixer')
        self.outputconvert = self.add_element('videoconvert')

        self.add_input_video_port_on(self.inputconvert)
        self.inputconvert.link(self.mixer)

        self.mixer.link(self.outputconvert)
        self.add_output_video_port_on(self.outputconvert)

        self.mixer.get_static_pad('sink_0').set_property('zorder', 0)

        self.alpha.set_value(1.0)

    def file_changed(self, new_file):
        print "Setting file:", new_file
        self.filesrc = self.add_element('filesrc')
        self.gdkdec = self.add_element('gdkpixbufdec')
        self.convert = self.add_element('videoconvert')
        self.freeze = self.add_element('imagefreeze')
        self.caps = self.add_element('capsfilter')
        caps = Gst.caps_from_string(self.DEFAULT_VIDEO_CAPS)
        self.caps.set_property('caps', caps)

        self.filesrc.set_property('location', new_file)

        self.filesrc.link(self.gdkdec)
        self.gdkdec.link(self.convert)
        self.convert.link(self.freeze)
        self.freeze.link(self.caps)
        videomixer_pad = self.mixer.get_request_pad("sink_%u")
        self.caps.get_static_pad('src').link(videomixer_pad)

        self.filesrc.set_state(Gst.State.PLAYING)
        self.gdkdec.set_state(Gst.State.PLAYING)
        self.convert.set_state(Gst.State.PLAYING)
        self.freeze.set_state(Gst.State.PLAYING)
        self.caps.set_state(Gst.State.PLAYING)

        videomixer_pad.set_property('zorder', 1)

    def alpha_changed(self, alpha):
        pass
        # self.overlay.set_property('alpha', alpha)
