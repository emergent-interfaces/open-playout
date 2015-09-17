import gi
import sys
from device import Device
from observable_variable import ObservableVariable

from control_panels.switcher_control_panel import SwitcherControlPanel

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class Switcher(Device):
    suggested_name = "switcher"
    suggested_readable_name = "Switcher"

    def __init__(self, name, inputs):
        Device.__init__(self, name)
        self.ControlPanelClass = SwitcherControlPanel

        self.program_active_id = ObservableVariable(0)
        self.preview_active_id = ObservableVariable(0)
        self.opacity = ObservableVariable(1.0)

        # Create elements that exist for all instances of the switcher
        self.prog_mixer = Gst.ElementFactory.make('videomixer', None)
        self.bin.add(self.prog_mixer)

        self.prev_mixer = Gst.ElementFactory.make('videomixer', None)
        self.bin.add(self.prev_mixer)

        # Add outputs for static mixer pads
        self.add_output_video_port_on(self.prog_mixer, "src", "prog_out")
        self.add_output_video_port_on(self.prev_mixer, "src", "prev_out")

        for input_id in range(inputs):
            # Create tee and create input
            tee = Gst.ElementFactory.make('tee', None)
            self.bin.add(tee)

            name = "in" + str(input_id + 1)

            self.add_input_video_port_on(tee, name, name)

            #pad = Gst.GhostPad.new(name, tee.get_static_pad("sink"))
            #self.bin.add_pad(pad)

            # Create queues
            queue1 = Gst.ElementFactory.make('queue', None)
            self.bin.add(queue1)
            queue2 = Gst.ElementFactory.make('queue', None)
            self.bin.add(queue2)

            # Link tee to queues
            pad = tee.get_request_pad("src_%u")
            toPad = queue1.get_static_pad("sink")
            pad.link(toPad)

            pad = tee.get_request_pad("src_%u")
            toPad = queue2.get_static_pad("sink")
            pad.link(toPad)

            # Link queues to videomixers
            pad = queue1.get_static_pad("src")
            toPad = self.prog_mixer.get_request_pad("sink_%u")
            pad.link(toPad)

            pad = queue2.get_static_pad("src")
            toPad = self.prev_mixer.get_request_pad("sink_%u")
            pad.link(toPad)

        if inputs >= 2:
            self.set_bus_input("preview", 1)
            self.set_bus_input("program", 0)
        else:
            self.set_bus_input("preview", 0)
            self.set_bus_input("program", 0)

        self.add_action("take", self.take, "Swap program and preview or set program")
        self.add_action("preview", self.preview, "Set preview")
        self.add_action("fade", self.fade, "Set fade position")

    def set_bus_input(self, bus, input_id):
        print "Setting bus input: " + bus + ", " + str(input_id)

        high_pad_name = "sink_" + str(input_id)

        if bus == "program":
            mixer = self.prog_mixer
            low_pad_name = "sink_" + str(self.preview_active_id.get_value())
            prev_high_pad_name = "sink_" + str(self.program_active_id.get_value())
        elif bus == "preview":
            mixer = self.prev_mixer
            low_pad_name = "sink_" + str(self.program_active_id.get_value())
            prev_high_pad_name = "sink_" + str(self.preview_active_id.get_value())
        else:
            return

        # Arrange input z-orders
        pad = mixer.get_static_pad(high_pad_name)
        pad.set_property('zorder', 2)

        pad = mixer.get_static_pad(low_pad_name)
        pad.set_property('zorder', 1)

        # Iterate over all sink pads and set below
        it = mixer.iterate_sink_pads()

        while True:
            status, pad = it.next()
            if status != Gst.IteratorResult.OK:
                break

            if (pad.get_name() != high_pad_name and pad.get_name() != low_pad_name):
                pad.set_property("zorder", 0)
                pad.set_property("alpha", 1.0)

        # Update
        if bus == "program":
            self.program_active_id.set_value(input_id)
        elif bus == "preview":
            self.preview_active_id.set_value(input_id)

        self.set_opacity(self.opacity.get_value())

        #self.debug_mixer(mixer)

    def debug_mixer(self, mixer):
        it = mixer.iterate_sink_pads()

        while True:
            status, pad = it.next()
            if status != Gst.IteratorResult.OK:
                break

            pad_info = "Pad: " + pad.get_name()
            pad_info = pad_info + " (zorder: " + str(pad.get_property("zorder"))
            pad_info = pad_info + ", alpha: " + str(pad.get_property('alpha')) + ")"
            print pad_info

    def take(self, program_id=None):
        if program_id is None:
            current_prog_id = self.program_active_id.get_value()
            current_prev_id = self.preview_active_id.get_value()

            self.set_bus_input("preview", current_prog_id)
            self.set_bus_input("program", current_prev_id)
        else:
            self.set_bus_input("program", int(program_id))

    def preview(self, preview_id):
        self.set_bus_input("preview", int(preview_id))

    def set_opacity(self, opacity):
        self.opacity.set_value(opacity)

        pad = self.prog_mixer.get_static_pad("sink_" + str(self.program_active_id.get_value()))

        if self.program_active_id.get_value() != self.preview_active_id.get_value():
            pad.set_property("alpha", opacity)
        else:
            pad.set_property("alpha", 1.0)

    def fade(self, opacity):
        self.set_opacity(float(opacity))
