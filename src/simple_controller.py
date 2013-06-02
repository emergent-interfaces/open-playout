import gi
import shlex
from gi.repository import GObject, Gtk, Gdk, GdkX11


class SimpleController(Gtk.Window):
    def __init__(self, station):
        Gtk.Window.__init__(self)
        self.station = station

        self.box = Gtk.Box(spacing=4, orientation=Gtk.Orientation.VERTICAL)
        self.box.set_homogeneous(False)
        self.add(self.box)

        self.entry = Gtk.Entry()
        self.box.pack_end(self.entry, False, True, 0)
        self.entry.connect('activate', self.on_entry_key_press)

        self.create_textview()
        self.entry.grab_focus()

        self.show_all()
        self.set_size_request(400, 300)

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        self.box.pack_end(scrolledwindow, True, True, 0)

        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textbuffer = self.textview.get_buffer()
        scrolledwindow.add(self.textview)

    def on_entry_key_press(self, widget, data=None):
        command = widget.get_text()
        if command != "":
            widget.set_text("")
            end_iter = self.textbuffer.get_end_iter()
            self.textbuffer.insert(end_iter, command + "\n")
            self.textview.scroll_to_iter(end_iter, 0, False, 0, 0)

            device_name, action, args = self.parse_command(command)
            self.perform_command(device_name, action, args)

    def parse_command(self, text):
        tokens = shlex.split(text)
        first_token = tokens.pop(0)

        if self.station.find_device_by_name(first_token):
            device_name = first_token
            action = tokens.pop(0)
            args = tokens
        else:
            device_name = None
            action = first_token
            args = tokens

        return device_name, action, args

    def perform_command(self, device_name, action, args):
        if device_name:
            device = self.station.find_device_by_name(device_name)
            device.do_action(action, args)
        else:
            for device in self.station.devices:
                device.do_action(action, args)

        if action == 'exit':
            self.station.stop()
            Gtk.main_quit()