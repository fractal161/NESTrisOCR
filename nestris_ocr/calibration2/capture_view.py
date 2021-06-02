from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class CaptureView(QGraphicsView):
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

  def refresh(self):
    self.scene().refresh()
    # Set sceneRect to something reasonable