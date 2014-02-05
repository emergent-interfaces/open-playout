import gi, os
from devices.link import Link

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst, GstVideo

class Station(object):
    def __init__(self, config, args):

        os.environ["GST_DEBUG"] = "2"
        Gst.init(None)

        self.pipeline = Gst.Pipeline()
        self.bus = self.pipeline.get_bus()

        self.devices = []
        self.links = []

        if args.graph:
            self.graph_pipeline()

    def graph_pipeline(self):
        Gst.debug_bin_to_dot_file(self.pipeline, Gst.DebugGraphDetails.ALL, "pipeline")
        try:
            os.system("dot -Tpng -o /tmp/pipeline.png /tmp/pipeline.dot")
        except Exception, e:
            print e

    def add_device(self, device):
        self.pipeline.add(device.get_bin())
        self.devices.append(device)
        device.set_playing()

    def remove_device(self, device):
        device.set_null()
        self.pipeline.remove(device.get_bin())
        self.devices.remove(device)

    def link(self, name, port_1, port_2):
        link = Link(name, port_1, port_2)
        print "Linking:", port_1, port_2
        self.pipeline.add(link.get_bin())
        link.set_playing()
        self.links.append(link)

    def unlink(self, port_1, port_2):
        link = self.find_link(port_1, port_2)
        link.set_null()
        self.pipeline.remove(link.get_bin())
        self.links.remove(link)

    def find_link(self, port_1, port_2):
        for link in self.links:
            if link.port_1 == port_1 and link.port_2 == port_2:
                return link

        return None        

    def find_device_by_name(self, name):
        for device in self.devices:
            if device.name == name:
                return device

        return None

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    # def assign_drawing_area(self, drawing_area, monitor_name):
    #     sink = self.find_device_by_name(monitor_name).get_sink()
    #     sink.set_window_handle(drawing_area.get_window().get_xid())