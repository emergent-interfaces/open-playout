self.install(VideoTestGen, "video1", (100, 100))
self.install(UstreamProvider, "ustream_provider1", (300, 100))
self.wire('video1.out', 'ustream_provider1.in')
