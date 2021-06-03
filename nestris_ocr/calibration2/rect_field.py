from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

'''
Initializing an x, y screws up the item coordinates.
To ensure the top-left is (0,0) in item coords, init the top-left to this and then call setTransform(QTransform.fromTranslate(x,y))
'''
class RectField(QGraphicsRectItem):
  '''Should overload this'''
  def __init__(self, color, x, y, width, height, *args, **kwargs):
    super().__init__(0, 0, width, height, *args, *kwargs)
    self.setTransform(QTransform.fromTranslate(x, y))
    self.setBrush(QBrush(color))
    self.setPen(QPen(QColor(Qt.transparent)))
    self.setFlag(QGraphicsItem.ItemIsMovable)

  def paint(self, painter, *args, **kwargs):
    super().paint(painter, *args, **kwargs)
    painter.setBrush(QBrush(QColor(255, 0, 0)))
    painter.drawRect(0,0,5,5)
    painter.drawRect(0,self.rect().height(),5,-5)
    painter.drawRect(self.rect().width(), self.rect().height(), -5, -5)
    painter.drawRect(self.rect().width(), 0, -5, 5)

  # def mousePressEvent(self, e):
  #   super().mousePressEvent(e)
  #   print(e.pos())
  #
  # def mouseReleaseEvent(self, e):
  #   super().mouseReleaseEvent(e)
  #   print(self.rect())

  # def mouseMoveEvent(self, e):
  #   super().mouseMoveEvent(e)
  #   print("Mousegrabber!")
  #   print(self.scene().mouseGrabberItem())