from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

from nestris_ocr.calibration2.draw_calibration import (
    draw_calibration,
    capture_das_trainer,
    capture_split_digits,
    capture_preview,
    capture_color1color2,
    capture_blackwhite,
)
from nestris_ocr.calibration2.rect_field import RectField

from nestris_ocr.capturing import uncached_capture
from nestris_ocr.config import config

from nestris_ocr.utils import xywh_to_ltrb
from nestris_ocr.utils.lib import (
    screenPercToPixels,
    lerp,
    mult_rect,
)
import os

# QPixmap(os.path.join(main_path, './boardLayout.png'))
class CaptureScene(QGraphicsScene):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.capture = QGraphicsPixmapItem()
    self.capture.setTransformationMode(Qt.SmoothTransformation)
    self.testRect = RectField(QColor(255, 0, 0, 127), 10, 10, 100, 100)
    self.testRect2 = RectField(QColor(0, 255, 0, 127), 150, 150, 70, 20)
    self.addItem(self.capture)
    self.addItem(self.testRect)
    self.addItem(self.testRect2)

  def refresh(self):
    main_path = os.path.dirname(__file__)
    # t = QTime()
    # t.start()
    im = draw_calibration(config)
    im = im.convert("RGBA")
    data = im.tobytes("raw","RGBA")
    qim = QImage(data, im.size[0], im.size[1], QImage.Format_RGBA8888)
    pix = QPixmap.fromImage(qim)
    # pix = ImageQt.toqpixmap(im)
    self.capture.setPixmap(pix)
    # print("no segfault?")
    self.setSceneRect(0,0,pix.width(), pix.height())
    # print(t.elapsed()/1000)

  def getCaptureArea(self, rect):
    im = QImage(self.capture.pixmap())
    if not isinstance(rect, QRect):
      rect = rect.toRect()
    return im.copy(rect)