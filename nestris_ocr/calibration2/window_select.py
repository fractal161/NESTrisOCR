from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# QGroupBox??????
class WindowSelect(QWidget):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.layout = QVBoxLayout()
    self.layout.setSpacing(0)
    self.layout.addWidget(DropDownField('Capture type:', ["Capture Card", "Window", "RTMP", "File"], self))
    self.layout.addWidget(TextField('Window prefix:', "", 20, self))
    self.layout.addWidget(TextField('Player name:', "", 20, self))
    self.layout.addStretch(1)

    self.setLayout(self.layout)

class TextField(QWidget):
  def __init__(self, label, default, maxLength, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.layout = QHBoxLayout()
    title = QLabel(label)
    self.layout.addWidget(title, Qt.AlignLeft)
    field = QLineEdit()
    field.setText(default)
    field.setMaxLength(maxLength)
    field.editingFinished.connect(lambda : print("Text changed to", field.text()))
    self.layout.addWidget(field, 0, Qt.AlignRight)

    self.setLayout(self.layout)

class DropDownField(QWidget):
    def __init__(self, label, items, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.layout = QHBoxLayout()
      title = QLabel(label)
      self.layout.addWidget(title, Qt.AlignLeft)
      combo = QComboBox()
      for item in items:
        combo.addItem(item)
      combo.currentTextChanged.connect(lambda x : print("Switched to", x))
      self.layout.addWidget(combo, 0, Qt.AlignRight)

      self.setLayout(self.layout)
    def setCurrentText(self, text):
      pass

