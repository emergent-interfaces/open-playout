import os

d, n = self.install(Deck, "deck1", (0, 0))
self.install(AudioOut, "audioout1", (300, 100))
self.install(Monitor, "monitor1", (300, 0))
self.wire('deck1.video_out', 'monitor1.in')
self.wire('deck1.audio_out', 'audioout1.in')

media = os.path.abspath(os.path.join(os.getcwd(), '../media'))
d.file_uri.set_value('file://' + media + '/sintel_trailer-480p.mp4')
