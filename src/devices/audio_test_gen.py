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

        self.src = Gst.ElementFactory.make('audiotestsrc', None)
        self.bin.add(self.src)

        #self.src2 = Gst.ElementFactory.make('audiotestsrc', None)
        #self.bin.add(self.src2)

        self.add_output_audio_port_on(self.src, "src")

        self.freqs = ObservableVariable([1000, 1000])
        self.freqs.changed.connect(self.change_freqs)

    def change_freqs(data):
        print data
