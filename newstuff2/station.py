import gi, os
from monitor import Monitor

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

        #self.build()

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

    def fix_connection(self):
        src = Gst.ElementFactory.make('videotestsrc', None)
        self.pipeline.add(src)

        convert = Gst.ElementFactory.make('videoconvert', None)
        self.pipeline.add(convert)

        intervideosink = Gst.ElementFactory.make('intervideosink', None)
        self.pipeline.add(intervideosink)

        caps = Gst.caps_from_string("video/x-raw,format=AYUV,width=320,height=240")

        print src.link(convert)
        print convert.link(intervideosink)

        src.set_state(Gst.State.PLAYING)
        convert.set_state(Gst.State.PLAYING)
        intervideosink.set_state(Gst.State.PLAYING)

        self.intervideosink = intervideosink

    def ruin_connection(self):
        self.intervideosink.set_state(Gst.State.READY)
        self.real_src.set_state(Gst.State.READY)

    def bring_it_back(self):
        self.intervideosink.set_state(Gst.State.PLAYING)
        self.real_src.set_state(Gst.State.PLAYING)

    def add(self):
        monitor = Monitor('monitor1', (320,240), (0,0))
        self.pipeline.add(monitor.get_bin())
        monitor.start_playing()
        self.devices.append(monitor)
        

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