#!/usr/bin/env python
# Using ppa: https://launchpad.net/~o-naudan/+archive/gst0.11

import gi
import sys
import station

from gi.repository import GObject, Gtk, Gdk, GdkX11

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
		
		self.video_window = Gtk.Window()
		self.drawing_area = Gtk.DrawingArea()
		self.video_window.add(self.drawing_area)
		self.drawing_area.show()
		self.drawing_area.connect("realize", self.on_video_window_realize)
		self.video_window.show_all()
	
	def on_video_window_realize(self, event):
		self.station.assign_drawing_area(self.drawing_area)
	
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
