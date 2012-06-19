#!/usr/bin/env python
# Using ppa: https://launchpad.net/~o-naudan/+archive/gst0.11

import gi
import sys

try:
	gi.require_version('Gst','1.0')
except ValueError:
	print 'Could not find required Gstreamer library'
	sys.exit(1)

from gi.repository import GObject, Gst, Gtk
print Gst.version_string()

class Main:
	def __init__(self):
		GObject.threads_init()
		Gst.init(None)
		
		self.pipeline = Gst.Pipeline()

		src = Gst.ElementFactory.make('v4l2src', None)
		caps_filter = Gst.ElementFactory.make('capsfilter', None)
		sink = Gst.ElementFactory.make('xvimagesink', None)

		caps_filter.set_property('caps',Gst.caps_from_string("video/x-raw, width=640, height=480"))

		self.pipeline.add(src)
		self.pipeline.add(caps_filter)
		self.pipeline.add(sink)

		src.link(caps_filter)
		caps_filter.link(sink)

		bus = self.pipeline.get_bus()
		bus.connect('message::eos', self.on_bus_eos)
		bus.connect('message', self.on_bus_message)
		bus.add_signal_watch()

	def on_bus_message(self, bus, message):
		print message
		print "here"
		
	def on_bus_eos(self, bus, message):
		print message
		print "eos"
		sys.exit(0)
		
	def run(self):
		self.pipeline.set_state(Gst.State.PLAYING)
		GObject.MainLoop().run()


if __name__ == "__main__":
	Main().run()
