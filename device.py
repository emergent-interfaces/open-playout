import gi
import sys

try:
	gi.require_version('Gst','1.0')
except ValueError:
	print 'Could not find required Gstreamer library'
	sys.exit(1)
	
from gi.repository import Gst

class Device(object):
	def __init__(self,name):
		self.name = name
		self.bin = Gst.Bin.new(self.name)

	def get_bin(self):
		return self.bin

	def get_port(self,name):
		return self.bin.get_static_pad(name)
