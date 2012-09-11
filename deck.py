import gi
import sys
import device
from os import path

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class Deck(device.Device):
    def __init__(self, name):
        device.Device.__init__(self, name)

        self.src = Gst.ElementFactory.make('uridecodebin', None)
        self.bin.add(self.src)

        filename = path.join(path.dirname(path.abspath(__file__)), 'test_media', 'clip1.mpg')
        uri = 'file://' + filename
        self.src.set_property('uri', uri)
        self.src.connect('pad-added', self.handle_new_pad)

        self.queue = Gst.ElementFactory.make('queue', None)
        self.bin.add(self.queue)

        ghost_pad = Gst.GhostPad.new("src", self.queue.get_static_pad("src"))
        self.bin.add_pad(ghost_pad)

    def handle_new_pad(self, element, pad, data=None):
        if "video" in pad.query_caps(None).to_string():
            pad.link(self.queue.get_static_pad("sink"))
