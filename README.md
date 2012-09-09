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