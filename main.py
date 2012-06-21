#!/usr/bin/env python
# Using ppa: https://launchpad.net/~o-naudan/+archive/gst0.11

import gi
import sys
import station

from gi.repository import GObject, Gtk

class Main:
	def __init__(self):
		GObject.threads_init()
		win = Gtk.Window()
		button = Gtk.Button(label="Swap")
		button.connect("clicked", self.on_swap)
		win.add(button)
		win.show_all()
		
		win.connect("delete-event", self.on_quit)
		
		self.station = station.Station()
		
	def run(self):
		self.station.run()
		Gtk.main()
		
	def on_quit(self, event, user_data):
		self.station.stop()
		Gtk.main_quit()
		
	def on_swap(self, widget):
		self.station.swap()

if __name__ == "__main__":
	Main().run()
