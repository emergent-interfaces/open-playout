#!/usr/bin/env python
# Using ppa: https://launchpad.net/~o-naudan/+archive/gst0.11

import gi
import sys
import station
import json
import argparse
import os

import config_parse
from devices.monitor import Monitor
from simple_controller import SimpleController

from gi.repository import GObject, Gtk, Gdk, GdkX11

os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/tmp"
os.putenv('GST_DEBUG_DUMP_DIR_DIR', '/tmp')


class Main:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-g', '--graph',
            help="Generate graph of pipeline",
            action='store_true')
        args = parser.parse_args()

        GObject.threads_init()

        config_text = open('config.json').read()
        self.config = json.loads(config_text)

        self.station = station.Station(self.config, args)

        controller = SimpleController(self.station)
        controller.connect("delete-event", self.on_quit)

        # Create displays for all monitors
        self.displays = {}
        for monitor in self.station.find_all_monitors():
            self.create_display(monitor.name, monitor.size, monitor.location)

    def create_display(self, name, size, location):
        display_window = Gtk.Window()
        self.displays[name] = display_window
        display_window.set_title(name)

        drawing_area = Gtk.DrawingArea()
        drawing_area.connect("realize", self.on_video_window_realize, name)

        display_window.add(drawing_area)
        drawing_area.show()
        display_window.show_all()

        if size == "full":
            display_window.fullscreen()
        else:
            width, height = config_parse.extract_axb(size, 320, 240)
            drawing_area.set_size_request(width, height)

        left, top = config_parse.extract_axb(location)
        if left != None and top != None:
            display_window.move(left, top)

    def on_video_window_realize(self, drawing_area, monitor):
        self.station.assign_drawing_area(drawing_area, monitor)

    def run(self):
        self.station.run()
        Gtk.main()

    def on_quit(self, event, user_data):
        self.station.stop()
        Gtk.main_quit()

if __name__ == "__main__":
    main = Main()
    main.run()
