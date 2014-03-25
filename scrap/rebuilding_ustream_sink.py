import os
import gi
try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)
from gi.repository import GObject, Gst

os.environ["GST_DEBUG"] = "4"
os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/tmp"
os.putenv('GST_DEBUG_DUMP_DIR_DIR', '/tmp')

GObject.threads_init()
Gst.init(None)

pipeline = Gst.Pipeline()
bus = pipeline.get_bus()

bin = Gst.Bin.new("bin1")

video_src = Gst.ElementFactory.make('videotestsrc', None)
bin.add(video_src)

video_input_queue = Gst.ElementFactory.make('queue', None)
bin.add(video_input_queue)

videoconvert = Gst.ElementFactory.make('videoconvert', None)
bin.add(videoconvert)

videoencoder = Gst.ElementFactory.make('x264enc', None)
bin.add(videoencoder)
videoencoder.set_property('bitrate', 4000)
videoencoder.set_property('bframes', 0)

videoparse = Gst.ElementFactory.make('h264parse', None)
bin.add(videoparse)

videoparse_queue = Gst.ElementFactory.make('queue', None)
bin.add(videoparse_queue)

flvmux = Gst.ElementFactory.make('flvmux', None)
bin.add(flvmux)
flvmux.set_property('streamable', True)

flvmux_queue = Gst.ElementFactory.make('queue', None)
bin.add(flvmux_queue)

rtmpsink = Gst.ElementFactory.make('fakesink', None)
bin.add(rtmpsink)

# Link elements
video_src.link(video_input_queue)
video_input_queue.link(videoconvert)
videoconvert.link(videoencoder)
videoencoder.link(videoparse)
videoparse_caps = Gst.caps_from_string('video/x-h264,level=(string)4.1,profile=main')
videoparse.link_filtered(videoparse_queue, videoparse_caps)
videoparse_queue.link(flvmux)
flvmux.link(flvmux_queue)
flvmux_queue.link(rtmpsink)

# Add to pipeline
pipeline.add(bin)
pipeline.set_state(Gst.State.PLAYING)



def blocked_for_replacing_rtmpsink(pad, info, data):
    flvmux_queue = data[2]
    rtmpsink = data[3]
    bin = data[4]

    flvmux_queue.unlink(rtmpsink)
    bin.remove(rtmpsink)
    rtmpsink.set_state(Gst.State.NULL)

    rtmpsink = Gst.ElementFactory.make('rtmpsink', None)
    bin.add(rtmpsink)
    rtmpsink.set_property('location', data[0] + "/" + data[1])

    flvmux_queue.link(rtmpsink)
    
    rtmpsink.set_state(Gst.State.PLAYING)

    print info.id

    pad.remove_probe(info.id)
    print "leaving callback"

def change_to_rtmp(url, key):
    flvmux_queue.get_static_pad('src').add_probe(
        Gst.PadProbeType.BLOCK_DOWNSTREAM,
        blocked_for_replacing_rtmpsink,
        [url, key, flvmux_queue, rtmpsink, bin]
    )

cmd = ""
while cmd != "exit":
    cmd = raw_input('>>> ')
    
    if cmd == "graph":
        Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL, "pipeline")
        os.system("dot -Tpng -o /tmp/pipeline.png /tmp/pipeline.dot")

    if cmd == "go":
        change_to_rtmp(
            'rtmp://1.17250770.fme.ustream.tv/ustreamVideo/17250770',
            'kXwZhqDthBKhMmetYxFwbMh7MAq5yV4N'
        )