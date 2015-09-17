print "Loading Configuration"

# Simple test
# self.install(VideoTestGen, "video1", (100, 100))
# self.install(Monitor, "screen1", (300, 100))
# self.wire('video1.out', 'screen1.in')
import os

# Switcher control panel test
# self.install(VideoTestGen, "video1", (0,0))
# d, n = self.install(VideoTestGen, "video2", (0,100))
# d.pattern.set_value(1)
# self.install(Switcher, "switcher1", (200,0))
# self.install(Monitor, "program", (400,0))
# d, n = self.install(Monitor, "preview", (400,100))
# d.location.set_value((330, 0))
# self.wire('video1.out', 'switcher1.in1')
# self.wire('video2.out', 'switcher1.in2')
# self.wire('switcher1.prog_out', 'program.in')
# self.wire('switcher1.prev_out', 'preview.in')

# Overlay test
self.install(VideoTestGen, "video1", (100, 100))
d, n = self.install(Dsk, "dsk1", (300, 100))
d.file.set_value('../media/lower_third.svg')
self.install(Monitor, "screen1", (500, 100))
self.wire('video1.out', 'dsk1.in')
self.wire('dsk1.out', 'screen1.in')

# # UStream Test
# self.install(VideoTestGen, "video1", (100, 100))
# self.install(UstreamProvider, "ustream_provider1", (300, 100))
# self.wire('video1.out', 'ustream_provider1.in')

# # Audio Test
# self.install(AudioTestGen, "testgen1", (100, 100))
# self.install(AudioOut, "audioout1", (300, 100))
# self.wire('testgen1.out', 'audioout1.in')

# # Deck Test
# d, n = self.install(Deck, "deck1", (0,0))
# self.install(AudioOut, "audioout1", (300, 100))
# self.install(Monitor, "monitor1", (300,0))
# self.wire('deck1.video_out', 'monitor1.in')
# self.wire('deck1.audio_out', 'audioout1.in')

# media = os.path.abspath(os.path.join(os.getcwd(), '../media'))
# d.file_uri.set_value('file://' + media + '/sintel_trailer-480p.mp4')
