from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class IntRange(QWidget):

  valueChanged = pyqtSignal(int)

  def __init__(self, label, min, max, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.layout = QHBoxLayout()
    title = QLabel(label)
    self.layout.addWidget(title)

    self.slider = QSlider(Qt.Horizontal)
    self.slider.setMinimum(min)
    self.slider.setMaximum(max)
    self.layout.addWidget(self.slider)

    self.number = QSpinBox()
    self.number.setMinimum(min)
    self.number.setMaximum(max)
    self.layout.addWidget(self.number)

    self.slider.valueChanged.connect(lambda x : self._valueChanged(x))
    self.number.valueChanged.connect(lambda x : self._valueChanged(x))

    self.setLayout(self.layout)

  @pyqtSlot(int)
  def _valueChanged(self, value):
    self.slider.setValue(value)
    self.number.setValue(value)
    self.valueChanged.emit(value)


class MsRange(QWidget):
  def __init__(self, label ,min, max, step, *args, **kwargs):
    super().__init__(*args, **kwargs)