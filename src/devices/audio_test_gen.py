import gi
import sys
from device import Device
from observable_variable import ObservableVariable

from control_panels.audio_test_gen_control_panel import AudioTestGenControlPanel

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class AudioTestGen(Device):
    suggested_name = "audiotestgen"
    suggested_readable_name = "Audio Test Generator"

    def __init__(self, name):
        Device.__init__(self, name)
        self.ControlPanelClass = AudioTestGenControlPanel

        self.freqs = ObservableVariable([1000, 1000])
        self.freqs.changed.connect(self.change_freqs)

        caps = Gst.caps_from_string(self.SINGLE_CHANNEL_AUDIO_CAPS)

        self.src0 = Gst.ElementFactory.make('audiotestsrc', None)
        self.bin.add(self.src0)
        self.src0.set_property('is-live', True)

        self.src1 = Gst.ElementFactory.make('audiotestsrc', None)
        self.bin.add(self.src1)
        self.src1.set_property('is-live', True)

        self.interleave = Gst.ElementFactory.make('interleave', None)
        self.bin.add(self.interleave)

        self.src0.link_filtered(self.interleave, caps)
        self.src1.link_filtered(self.interleave, caps)

        self.add_output_audio_port_on(self.interleave, "src")

        self.change_freqs(self.freqs.get_value())

    def change_freqs(self, data):
        self.src0.set_property('freq', data[0])
        self.src1.set_property('freq', data[1])
