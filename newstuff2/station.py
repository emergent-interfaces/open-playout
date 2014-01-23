import gi, os
from monitor import Monitor
from video_test_gen import VideoTestGen

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst, GstVideo

class Station(object):
    def __init__(self, config, args):

        os.environ["GST_DEBUG"] = "3"
        Gst.init(None)

        self.pipeline = Gst.Pipeline()
        self.bus = self.pipeline.get_bus()

        self.devices = []

        if args.graph:
            self.graph_pipeline()

    def graph_pipeline(self):
        Gst.debug_bin_to_dot_file(self.pipeline, Gst.DebugGraphDetails.ALL, "pipeline")
        try:
            os.system("dot -Tpng -o /tmp/pipeline.png /tmp/pipeline.dot")
        except Exception, e:
            print e

    # Build a test pipeline
    def build(self):
        intervideosrc = Gst.ElementFactory.make('intervideosrc', None)
        self.pipeline.add(intervideosrc)

        convert = Gst.ElementFactory.make('videoconvert', None)
        self.pipeline.add(convert)

        image_sink = Gst.ElementFactory.make('xvimagesink', None)
        self.pipeline.add(image_sink)

        intervideosrc.link(convert)
        convert.link(image_sink)

    def add_device(self, device):
        self.pipeline.add(device.get_bin())
        self.devices.append(device)
        device.set_playing()

    def remove_device(self, device):
        device.set_null()
        self.pipeline.remove(device.get_bin())
        self.devices.remove(device)        

    def find_device_by_name(self, name):
        for device in self.devices:
            if device.name == name:
                return device

        return None

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def assign_drawing_area(self, drawing_area, monitor_name):
        sink = self.find_device_by_name(monitor_name).get_sink()
        sink.set_window_handle(drawing_area.get_window().get_xid())