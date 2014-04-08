import gi
import sys
from device import Device

try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer library'
    sys.exit(1)

from gi.repository import Gst


class Link(Device):
    def __init__(self, name, channel1, channel2, media_type):
        Device.__init__(self, name)

        if media_type == 'video':
            intersrc = 'intervideosrc'
            intersink = 'intervideosink'
            intercaps = self.DEFAULT_VIDEO_CAPS
        else:
            intersrc = 'interaudiosrc'
            intersink = 'interaudiosink'
            intercaps = self.DEFAULT_AUDIO_CAPS

        src = Gst.ElementFactory.make(intersrc, None)
        self.port_1 = channel1
        src.set_property('channel', channel1)
        self.bin.add(src)

        sink = Gst.ElementFactory.make(intersink, None)
        self.port_2 = channel2
        sink.set_property('channel', channel2)
        self.bin.add(sink)

        src.link_filtered(sink, Gst.caps_from_string(intercaps))
