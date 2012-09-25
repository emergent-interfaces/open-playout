import gi
import sys

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)


class Patch(object):
    def __init__(self, src, sink):
        self.src = src
        self.sink = sink

        self.src.link(self.sink)
