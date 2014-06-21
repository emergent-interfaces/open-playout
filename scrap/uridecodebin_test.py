import os
import gi
try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)
from gi.repository import GObject, Gst

from devices.monitor import Monitor
from display import Display

os.environ["GST_DEBUG"] = "1"
os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/tmp"
os.putenv('GST_DEBUG_DUMP_DIR_DIR', '/tmp')

def on_new_decoded_pad(decodebin, pad):
    caps_string = pad.get_current_caps().to_string()

    print "New pad:", caps_string

    if "video/x-raw" in caps_string:
        pad.link(vsink.get_static_pad("sink"))

    #if "audio/x-raw" in caps_string:
    #    pad.link(self.audio_queue.get_static_pad("sink"))

GObject.threads_init()
Gst.init(None)

pipeline = Gst.Pipeline()
bus = pipeline.get_bus()


device = Monitor("monitor1", (320, 240), (0, 0))
device.display = Display(self, device)

bin = Gst.Bin.new("bin1")

vsink = Gst.ElementFactory.make('xvimagesink', None);
bin.add(vsink)

decodebin = Gst.ElementFactory.make('uridecodebin', None)
bin.add(decodebin)
decodebin.connect("pad-added", on_new_decoded_pad)
#decodebin.connect("no-more-pads", self.on_no_more_pads)


pipeline.add(bin)
pipeline.set_state(Gst.State.PLAYING)

cmd = ""
while cmd != "exit":
    cmd = raw_input('>>> ')
    
    if cmd == "graph":
        Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL, "pipeline")
        os.system("dot -Tpng -o /tmp/pipeline.png /tmp/pipeline.dot")

    if cmd == "go":
        decodebin.set_property('uri', 'file:///home/lsimons/workspace/open-playout/media/3wanderings.mpg')