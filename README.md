Open Playout
============
An open source playout and live compositing tool.  This might be the
fourth time I've rebooted this project.  Sorry to anyone who's had any
hope in the previous versions.

Setting Up Development System
=============================
These instructions are applicable to Ubuntu 13.10.  They are heavily borrowed
from the [Novacut wiki](https://wiki.ubuntu.com/Novacut/GStreamer1.0#Adding_PPA_for_Ubuntu_Precise).

    sudo apt-add-repository ppa:gstreamer-developers/ppa
    sudo apt-get update

    sudo apt-get install python-gi python3-gi \
        gstreamer1.0-tools \
        gir1.2-gstreamer-1.0 \
        gir1.2-gst-plugins-base-1.0 \
        gstreamer1.0-plugins-good \
        gstreamer1.0-plugins-ugly \
        gstreamer1.0-plugins-bad \
        gstreamer1.0-libav

You'll also need QT and PySide.  If you are using a debugger like gdb, you'll want to install the debug symbols for each library.

Designing a Station
===================
Right click on the gray canvas to add devices to your station.  Drag wires from port to port to connect devices.  In lieu of any sort of save file, there is a `config.py` that is executed at start-up where you can construct a station manually.  For example:

    self.install(VideoTestGen, "video1", (100, 100))
    self.install(Monitor, "screen1", (300, 100))
    self.wire('video1.out', 'screen1.in')

Install a device by providing a device class, device name, and location on the station canvas.  The configuration file is simply executed by Python, so it exposes all the functionality of the devices.  Each install returns the device and node (visual representation of the device on the canvas) which can be used.  For example:

    self.install(VideoTestGen, "video1", (100, 100))
    d, n = self.install(Dsk, "dsk1", (300, 100))
    d.file.set_value('../media/lower_third.svg')
    self.install(Monitor, "screen1", (500, 100))
    self.wire('video1.out', 'dsk1.in')
    self.wire('dsk1.out', 'screen1.in')

Devices
=======
A limited set of devices are functional to some extent.  The current devices are:

* Camera - presents the output of a V4L2 source
* Dsk - down stream key to overlay a PNG or SVG file
* Monitor - output to send video to a window or screen
* Switcher - choose between a set of video streams
* VideoTestGen - generates a test video pattern

Creating New Devices
--------------------
A device is just a Gstreamer `bin` where the inputs and outputs are presented by the `inter` series of elements.  This allows plugging components together at run-time without crashing the pipeline.