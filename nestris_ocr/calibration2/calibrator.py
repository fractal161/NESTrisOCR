from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from nestris_ocr.capturing import uncached_capture
from nestris_ocr.calibration2.number_range import IntRange
from nestris_ocr.calibration2.window_select import WindowSelect
from nestris_ocr.calibration2.capture_scene import CaptureScene
from nestris_ocr.calibration2.capture_view import CaptureView

import os

class Calibrator(QMainWindow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.initUI()
    self.setFocusPolicy(Qt.StrongFocus)
    self.show()

  # NEED DEFAULT ACTIONS FOR SOME OF THESE
  def _setupActions(self):
    fieldNames = ['Level', 'Score', 'Lines', 'Board', 'Colors', 'Preview', 'Flash capture', 'Black/White', 'Piece stats', 'DAS Trainer']
    self.fieldActs = QActionGroup(self)
    for name in fieldNames:
      act = QAction(name, self)
      act.setCheckable(True)
      self.fieldActs.addAction(act)

    presetNames = ['Custom', 'Standalone', 'Nestris99']
    presetTips = ['', '', '']
    self.presetActs = QActionGroup(self)
    for name in presetNames:
      act = QAction(name, self)
      act.setCheckable(True)
      self.presetActs.addAction(act)

    self.hexAct = QAction('Hex Score Support', self)
    self.hexAct.setStatusTip('Scores past 999999 as A00000 to F99999')
    self.hexAct.setCheckable(True)

    self.bwAct = QAction('Black/White')
    self.bwAct.setCheckable(True)

    self.boardAct = QAction('Capture game field', self)
    self.boardAct.setCheckable(True)

    self.nextAct = QAction('Capture next piece', self)
    self.nextAct.setCheckable(True)

    self.statsAct = QAction('Capture piece stats', self)
    self.statsAct.setCheckable(True)

    pieceCapNames = ['Text', 'Field']
    pieceCapTips = ['', '']
    self.pieceCapActs = QActionGroup(self)
    for name in pieceCapNames:
      act = QAction(name, self)
      act.setCheckable(True)
      self.pieceCapActs.addAction(act)

    flashNames = ['Background', 'Field', 'None']
    flashTips = ['', '', '']
    self.flashActs = QActionGroup(self)
    for name in flashNames:
      act = QAction(name, self)
      act.setCheckable(True)
      self.flashActs.addAction(act)

    self.colorAct = QAction('Capture colors', self)
    self.colorAct.setStatusTip('Detect colors from the capture. Leave unchecked if using a layout without piece statistics.')
    self.colorAct.setCheckable(True)

  def _setupMenu(self):
    menu = self.menuBar()
    fields = menu.addMenu('&Fields')
    for act in self.fieldActs.actions():
      fields.addAction(act)
    options = menu.addMenu('&Options')
    preset = options.addMenu('Preset')
    for act in self.presetActs.actions():
      preset.addAction(act)
    options.addAction(self.hexAct)
    options.addAction(self.bwAct)
    options.addAction(self.boardAct)
    options.addAction(self.nextAct)
    options.addAction(self.statsAct)
    pieceCap = options.addMenu('Piece stats capture method')
    for act in self.pieceCapActs.actions():
      pieceCap.addAction(act)
    flash = options.addMenu('Flash capture method')
    for act in self.flashActs.actions():
      flash.addAction(act)
    options.addAction(self.colorAct)

  def initUI(self):
    main_path = os.path.dirname(__file__)
    self._setupActions()
    self._setupMenu()
    statusbar = self.statusBar()
    statusbar.setStyleSheet('QStatusBar{border-top: 1px outset grey;}')

    self.windowSelect = WindowSelect()

    self.buttonStack = QVBoxLayout()
    self.buttonStack.setSpacing(0)
    self.buttonStack.addWidget(QPushButton('Simple Mode'))
    self.buttonStack.addWidget(QPushButton('Auto Calibrate'))
    self.buttonStack.addWidget(QPushButton('Refresh Image'))
    # self.buttonStack.addStretch(1)
    buttons = QWidget()
    buttons.setLayout(self.buttonStack)

    self.topBoxLayout = QHBoxLayout()
    self.topBoxLayout.addWidget(self.windowSelect)
    self.topBoxLayout.addWidget(buttons)

    # self.view = QLabel(self)
    # pixmap = QPixmap(os.path.join(main_path, './boardLayout.png'))
    # pixmap = pixmap.scaled(2*pixmap.width(), 2*pixmap.height())
    # self.view.setPixmap(pixmap)
    self.scene = CaptureScene()
    self.view = CaptureView(self.scene)
    # Necessary as an offering to the sizeHint overlords
    self.view.refresh()
    self.view.fitInView(self.view.sceneRect(), Qt.KeepAspectRatio)

    self.leftLayout = QVBoxLayout()
    self.topLeft = QWidget()
    self.topLeft.setLayout(self.topBoxLayout)
    self.leftLayout.addWidget(self.topLeft)
    # self.leftLayout.addWidget(self.capture)
    self.leftLayout.addWidget(self.view)

    self.captureDims = QGroupBox("Capture dimensions")
    self.dimLayout = QVBoxLayout()
    self.captureX = IntRange('x', 0, 1000)
    self.captureY = IntRange('y', 0, 1000)
    self.captureW = IntRange('w', 0, 1000)
    self.captureH = IntRange('h', 0, 1000)

    self.dimLayout.addWidget(self.captureX)
    self.dimLayout.addWidget(self.captureY)
    self.dimLayout.addWidget(self.captureW)
    self.dimLayout.addWidget(self.captureH)
    self.dimLayout.addStretch(1)
    self.captureDims.setLayout(self.dimLayout)
    # self.leftLayout.addWidget(self.captureDims)

    self.left = QWidget(self)
    self.left.setLayout(self.leftLayout)

    self.right = QTabWidget(self)
    self.test = QLabel(self)
    # pixmap = QPixmap(os.path.join(main_path, './boardLayout.png'))
    # pixmap = pixmap.scaled(2*pixmap.width(), 2*pixmap.height())
    self.view.rectChanged.connect(lambda x, y : self.test.setPixmap(QPixmap(y)))
    # self.test.setPixmap(pixmap)
    self.right.addTab(self.test, 'Test')

    self.layout = QHBoxLayout()
    self.layout.addWidget(self.left)
    self.layout.addWidget(self.right)
    self.main = QWidget(self)
    self.main.setLayout(self.layout)
    self.setCentralWidget(self.main)
    # self.resize(pixmap.width(), pixmap.height())
    self.timer = QTimer()
    self.timer.timeout.connect(self.view.refresh)
    self.timer.start(50)

  def show(self, *args, **kwargs):
    super().show(*args, **kwargs)
    self.view.setRect(self.view.sceneRect())


  def resizeEvent(self, *args, **kwargs):
    super().resizeEvent(*args, **kwargs)
    # self.view.refresh()
    # print(self.view.width(), self.view.height())
    self.view.setRect(self.view.sceneRect())
    # print(self.view.transform().type())
    # print(self.view.mapFromScene(0.0,0.0))
    # print(self.view.mapToScene(self.view.viewport().width(), self.view.viewport().height()))
    # print(self.view.viewport().width(), self.view.viewport().height())
    # print(self.width(), self.height())

  def closeEvent(self, *args, **kwargs):
    super().closeEvent(*args, **kwargs)
    uncached_capture().stop()
    # stop the uncached capture.