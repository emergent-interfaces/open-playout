import os, sys, argparse
import PySide
from PySide.QtGui import QApplication, QMessageBox
import gi
from gi.repository import GObject

from station import Station

os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/tmp"
os.putenv('GST_DEBUG_DUMP_DIR_DIR', '/tmp')

class Main:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-g', '--graph',
            help="Generate graph of pipeline",
            action='store_true')
        args = parser.parse_args()

        GObject.threads_init()

        self.station = Station({}, args)

    def run(self):
        self.station.run()

        app = QApplication(sys.argv)
        msgBox = QMessageBox()
        msgBox.exec_()

        self.station.fix_connection()

        msgBox = QMessageBox()
        msgBox.exec_()

if __name__ == "__main__":
    main = Main()
    main.run()