import gi
import sys
from device import Device
from observable_variable import ObservableVariable
from control_panels.ustream_provider_control_panel import UstreamProviderControlPanel

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class UstreamProvider(Device):
    suggested_name = "ustream_provider"
    suggested_readable_name = "UStream Provider"

    def __init__(self, name):
        Device.__init__(self, name)
        self.ControlPanelClass = UstreamProviderControlPanel

        self.url_and_key = ObservableVariable([None, None])
        self.url_and_key.changed.connect(self.change_url_and_key)

        self.video_input_queue = Gst.ElementFactory.make('queue', None)
        self.bin.add(self.video_input_queue)

        self.videoconvert = Gst.ElementFactory.make('videoconvert', None)
        self.bin.add(self.videoconvert)

        self.videoencoder = Gst.ElementFactory.make('x264enc', None)
        self.bin.add(self.videoencoder)
        self.videoencoder.set_property('bitrate', 4000)
        self.videoencoder.set_property('bframes', 0)

        self.videoparse = Gst.ElementFactory.make('h264parse', None)
        self.bin.add(self.videoparse)

        self.videoparse_queue = Gst.ElementFactory.make('queue', None)
        self.bin.add(self.videoparse_queue)

        self.flvmux = Gst.ElementFactory.make('flvmux', None)
        self.bin.add(self.flvmux)
        self.flvmux.set_property('streamable', True)

        self.flvmux_queue = Gst.ElementFactory.make('queue', None)
        self.bin.add(self.flvmux_queue)

        self.rtmpsink = Gst.ElementFactory.make('fakesink', None)
        self.bin.add(self.rtmpsink)

        # Link elements
        self.video_input_queue.link(self.videoconvert)
        self.videoconvert.link(self.videoencoder)
        self.videoencoder.link(self.videoparse)
        videoparse_caps = Gst.caps_from_string('video/x-h264,level=(string)4.1,profile=main')
        self.videoparse.link_filtered(self.videoparse_queue, videoparse_caps)
        self.videoparse_queue.link(self.flvmux)
        self.flvmux.link(self.flvmux_queue)
        self.flvmux_queue.link(self.rtmpsink)

        # Add ports
        self.add_input_port_on(self.video_input_queue, "sink")

    def change_url_and_key(self, url_and_key):
        self.flvmux_queue.get_static_pad('src').add_probe(
            Gst.PadProbeType.BLOCK_DOWNSTREAM,
            self.blocked_for_replacing_rtmpsink,
            url_and_key
        )

    def blocked_for_replacing_rtmpsink(self, pad, info, data):
        self.flvmux_queue.unlink(self.rtmpsink)
        self.bin.remove(self.rtmpsink)
        self.rtmpsink.set_state(Gst.State.NULL)
        del self.rtmpsink

        if data[0] and data[1]:
            self.rtmpsink = Gst.ElementFactory.make('rtmpsink', None)
            self.bin.add(self.rtmpsink)
            self.rtmpsink.set_property('location', data[0] + "/" + data[1])
        else:
            self.rtmpsink = Gst.ElementFactory.make('fakesink', None)
            self.bin.add(self.rtmpsink)

        self.flvmux_queue.link(self.rtmpsink)
        
        self.rtmpsink.set_state(Gst.State.PLAYING)

        pad.remove_probe(info.id)