Open Playout
============
An open source playout and live compositing tool.  This might be the
third time I've rebooted this project.  Sorry to anyone who's had any
hope in the previous versions.

Setting Up Development System
=============================
These instructions are applicable to Ubuntu 12.04.  They are heavily borrowed
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

Designing a Station
===================
The config.json file is used to design your station's initial setup.  A station is built by linking various devices together by patches.  An empty configuration follows:

    {
        "devices": [],
        "patches": []
    }

Devices are specified as dictionaries containing their setup details.  For example:

    {"type": "deck", "name": "main_deck"}

All device dictionaries must specifiy at least a device type and name.  Most devices require additional parameters to be specified.

To connect devices, patch dictionaries specifiy connections in the form `device_name.device_port`.  For example:

    {"src": "deck1.src", "sink": "program_monitor.sink"}

Devices
=======
These devices are working, functional to some extent, patently broken, drafts, or ideas threatening to become any of those previous options.  Also, you would think that parameters that aren't the most basic ones would have defaults if they aren't specified.  That's probably not the case right now.

Monitor
-------
* type:     "monitor"
* name
* size:     For a windowed monitor, width and height in the format "widthxheight" like "320x240".
            For a fullscreen window, specify "full".
* location: The offset from top and left of the primary display in the format "widthxheight".

Camera
------
* type:     "camera"
* name

Deck
----
* type:     "deck"
* name

VideoTestGen
------------
* type:     "video_test_gen"
* name
* pattern:  Integer corresponding to [GstVideoTestSrcPattern](http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-videotestsrc.html#GstVideoTestSrcPattern).  Defaults to 0.

Switcher
--------
* type:     "switcher"
* name
* inputs:   Number of inputs to switch between

Mixer
-----
Not started

Character Generator
-------------------
Not started

Audio Output
------------
Not started