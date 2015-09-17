self.install(VideoTestGen, "video1", (100, 100))
self.install(Monitor, "screen1", (300, 100))
self.wire('video1.out', 'screen1.in')
