import gi
import sys

try:
	gi.require_version('Gst','1.0')
except ValueError:
	print 'Could not find required Gstreamer library'
	sys.exit(1)

from gi.repository import GObject, Gst

GObject.threads_init()
Gst.init(None)

sink = Gst.ElementFactory.make('fakesink', None)
bin = Gst.Bin.new('my_bin')
bin.add(sink)

pad = sink.get_static_pad('sink')
print pad
ghost_pad = Gst.GhostPad.new('src',pad)
print ghost_pad

bin.add_pad(ghost_pad)
