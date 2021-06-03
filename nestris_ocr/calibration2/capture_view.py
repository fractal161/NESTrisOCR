from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from nestris_ocr.calibration2.rect_field import RectField

class CaptureView(QGraphicsView):
  rectChanged = pyqtSignal([str, 'QImage'])

  def __init__(self, *args, **kwargs):
    super().__init__(*args, *kwargs)
    # self.setCacheMode(QGraphicsView.CacheBackground)
    self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

  def setRect(self, rect):
    self.setTransform(QTransform())
    self.scale(self.viewport().width() / max(1, self.sceneRect().width()), self.viewport().height() / max(1, self.sceneRect().height()))

  def addRectField(self):
    pass

  def mouseMoveEvent(self, e):
    super().mouseMoveEvent(e)
    # Get the rect that was moved, figure out its new dimensions
    field = self.scene().mouseGrabberItem()
    if field is None:
      return
    sceneRect = QRectF(field.mapToParent(field.rect().topLeft()), field.mapToParent(field.rect().bottomRight()))
    img = self.scene().getCaptureArea(sceneRect)
    # img.save('./test.png')
    # Emit signal sending name of the field along with its current image
    self.rectChanged.emit('test', img)


  @pyqtSlot()
  def refresh(self):
    self.scene().refresh()
    # Set sceneRect to something reasonable