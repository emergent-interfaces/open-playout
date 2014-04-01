# Requires librsvg2-dev, python-cairo
import gi
import sys
import cairo
from device import Device
from observable_variable import ObservableVariable
from control_panels.dsk_control_panel import DskControlPanel

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

        # self.convert1 = Gst.ElementFactory.make('videoconvert', None)
        # self.bin.add(self.convert1)

        self.overlay = Gst.ElementFactory.make('gdkpixbufoverlay', None)
        self.bin.add(self.overlay)

        # self.convert2 = Gst.ElementFactory.make('videoconvert', None)
        # self.bin.add(self.convert2)

        # self.convert1.link(self.overlay)
        # self.overlay.link(self.convert2)

        self.add_input_port_on(self.overlay)
        self.add_output_port_on(self.overlay)

        #self.overlay.connect("draw", self.draw)

        self.overlay.set_property('overlay_width', self.DEFAULT_VIDEO_WIDTH)
        self.overlay.set_property('overlay_height', self.DEFAULT_VIDEO_HEIGHT)

        self.alpha.set_value(1.0)
        
    def draw(self, element, ctx, arg2, arg3):
        print dir(ctx)
        ctx.move_to(1,1)

    def file_changed(self, new_file):
        try:
            with open(new_file):
                self.overlay.set_property('location', new_file)
        except IOError:
            print "Overlay file " + new_file + " not found"

    def alpha_changed(self, alpha):
        self.overlay.set_property('alpha', alpha)