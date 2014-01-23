import os, sys
import argparse
import gi
from gi.repository import GObject, Gtk, Gdk, GdkX11
from threading import Thread

from station import Station

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

        cmd = ""
        while cmd != "exit":
            cmd = raw_input('>>> ')
            self.parse(cmd)


    def parse(self, cmd):
        if cmd == "fix":
            self.station.fix_connection()

        if cmd == "ruin":
            self.station.ruin_connection()

        if cmd == "back":
            self.station.bring_it_back()

        if cmd == "add":
            self.station.add()
            #self.create_display('monitor1', (640, 480), (0,0))

        if cmd == "graph":
            self.station.graph_pipeline()

        if cmd == "exit":
            Gtk.main_quit()

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