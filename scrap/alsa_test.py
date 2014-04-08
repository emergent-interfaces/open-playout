import os
import gi
import sys
try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)
from gi.repository import GObject, Gst

os.environ["GST_DEBUG"] = "3"
os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/tmp"
os.putenv('GST_DEBUG_DUMP_DIR_DIR', '/tmp')

GObject.threads_init()
Gst.init(None)

pipeline = Gst.Pipeline()
bus = pipeline.get_bus()

# Sending
bin1 = Gst.Bin.new("bin1")
pipeline.add(bin1)

caps_string = "audio/x-raw,channels=(int)2,rate=(int)48000,format=(string)S16LE"
caps = Gst.caps_from_string(caps_string)

src1 = Gst.ElementFactory.make('audiotestsrc', None)
bin1.add(src1)
intersink = Gst.ElementFactory.make('interaudiosink', None)
bin1.add(intersink)

src1.link_filtered(intersink, caps)

# Receiving
bin2 = Gst.Bin.new("bin2")
pipeline.add(bin2)

intersrc = Gst.ElementFactory.make('interaudiosrc', None)
bin2.add(intersrc)

queue = Gst.ElementFactory.make('queue', None)
bin2.add(queue)

sink2 = Gst.ElementFactory.make('alsasink', None)
bin2.add(sink2)

intersrc.link_filtered(queue, caps)
queue.link(sink2)

# Done building
pipeline.set_state(Gst.State.PLAYING)

cmd = ""
while cmd != "exit":
    cmd = raw_input('>>> ')

    if cmd == "graph":
        Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL, "pipeline")
        os.system("dot -Tpng -o /tmp/pipeline.png /tmp/pipeline.dot")
