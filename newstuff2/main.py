import os, sys
import argparse
import gi
from gi.repository import GObject, Gtk, Gdk, GdkX11
import shlex
from threading import Thread

from station import Station
from monitor import Monitor
from video_test_gen import VideoTestGen

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
        Gdk.threads_init()

        self.station = Station({}, args)
        self.displays = {}

    def run(self):
        self.station.run()

        # Almost definitely have some issues with threading
        #Thread(target=self.terminal).start()

        self.terminal()

        #self.station.add()
        #self.station.fix_connection()
        #Gtk.main()

    def terminal(self):
        print "Open-Playout Server"

        self.test_cmd('add monitor m1')
        self.test_cmd('add videotestgen v1')
        #self.test_cmd('link v1.output m1.input')

        cmd = ""
        while cmd != "exit":
            cmd = raw_input('>>> ')
            self.parse(cmd)

    def parse(self, cmd):
        tokens = shlex.split(cmd)
        first_token = tokens.pop(0)

        if first_token == "add":
            device_type = tokens.pop(0)
            device_name = tokens.pop(0)

            if device_type == 'videotestgen':
                videotestgen = VideoTestGen(device_name)
                self.station.add_device(videotestgen)

            if device_type == 'monitor':
                monitor = Monitor(device_name, (320,240), (0,0))
                self.station.add_device(monitor)
                #self.create_display('monitor1', (640, 480), (0,0))

        if first_token == "remove":
            device_name = tokens.pop(0)
            self.station.remove_device(self.station.find_device_by_name(device_name))

        if first_token == "graph":
            self.station.graph_pipeline()

        if first_token == "link":
            device1, _, port1 = tokens.pop(0).partition('.')
            device2, _, port2 = tokens.pop(0).partition('.')
            self.station.link(device1, port1, device2, port2)

        if first_token == "exit":
            Gtk.main_quit()

    def test_cmd(self, cmd):
        print ">>>", cmd
        self.parse(cmd)

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
            width, height = size
            drawing_area.set_size_request(width, height)

        left, top = location
        if left != None and top != None:
            display_window.move(left, top)

    def on_video_window_realize(self, drawing_area, monitor):
        self.station.assign_drawing_area(drawing_area, monitor)

if __name__ == "__main__":
    main = Main()
    main.run()