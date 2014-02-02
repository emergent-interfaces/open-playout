import gi, os

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

        self.build()

        if args.graph:
            Gst.debug_bin_to_dot_file(self.pipeline, Gst.DebugGraphDetails.ALL, "pipeline")
            try:
                os.system("dot -Tpng -o /tmp/pipeline.png /tmp/pipeline.dot")
            except Exception, e:
                print e

    # Build a test pipeline
    def build(self):
        queue_normal = Gst.ElementFactory.make('queue', None)
        self.pipeline.add(queue_normal)
        self.queue_normal = queue_normal

        queue_fallback = Gst.ElementFactory.make('queue', None)
        self.pipeline.add(queue_fallback)

        fallback_src = Gst.ElementFactory.make('videotestsrc', None)
        self.pipeline.add(fallback_src)

        selector = Gst.ElementFactory.make('input-selector', None)
        self.pipeline.add(selector)

        convert = Gst.ElementFactory.make('videoconvert', None)
        self.pipeline.add(convert)

        image_sink = Gst.ElementFactory.make('xvimagesink', None)
        self.pipeline.add(image_sink)

        fallback_src.link(queue_fallback)

        queue_normal.link(selector)
        queue_fallback.link(selector)
        
        selector.link(convert)
        convert.link(image_sink)

        queue_normal.connect('underrun', self.fallback, selector)
        queue_normal.connect('running', self.standup, selector)

    def fallback(self, element, selector):
        print "Falling back!"
        selector.set_property('active-pad', selector.get_static_pad('sink_1'))

    def standup(self, element, selector):
        print "Standing up!"
        selector.set_property('active-pad', selector.get_static_pad('sink_0'))

    def fix_connection(self):
        real_src = Gst.ElementFactory.make('videotestsrc', None)
        real_src.set_property('pattern', 1)
        self.pipeline.add(real_src)

        real_src.link(self.queue_normal)
        real_src.set_state(Gst.State.PLAYING)

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)