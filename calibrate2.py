#!/usr/bin/python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys
from nestris_ocr.calibration2.calibrator import Calibrator
# from .simple_calibrator import SimpleCalibrator
from nestris_ocr.config import config

# def get_calibrator_type(config):
#     if config["calibrator.ui"] == "SIMPLE":
#         return SimpleCalibrator
#     elif config["calibrator.ui"] == "ADVANCED":
#         return Calibrator
#     else:
#         return Calibrator


# def mainLoop():
#     exit_program = False
#     while not exit_program:
#         Constructor = get_calibrator_type(config)
#         c = Constructor(config)
#         while not c.destroying:
#             c.update()
#             # needs to be called outside of c.update()
#             if c.exit_calibrator:
#                 exit_program = c.exit_program
#                 c.on_exit()
#         uncached_capture().stop()
#
#
# if __name__ == "__main__":
#     mainLoop()


class Debug(QApplication):

    t = QElapsedTimer()

    def notify(self, receiver, event):
        self.t.start()
        ret = QApplication.notify(self, receiver, event)
        if(self.t.elapsed() > 1):
            print(f"processing event type {event.type()} for object {receiver.objectName()} "
                  f"took {self.t.elapsed()}ms")
        return ret


def main():
  # app = Debug(sys.argv)
  app = QApplication(sys.argv)
  ex = Calibrator()
  sys.exit(app.exec_())


if __name__ == '__main__':
    main()
