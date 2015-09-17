self.install(AudioTestGen, "testgen1", (100, 100))
self.install(AudioOut, "audioout1", (300, 100))
self.wire('testgen1.out', 'audioout1.in')
