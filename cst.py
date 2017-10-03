from airfoil_module import CST, create_x
import sys
import os 
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy
from PyQt4 import QtGui, QtCore

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	GUI.show()
	sys.exit(app.exec_())

def CSTMOD():

	chord = 1.
	x = create_x(chord, n = 20, distribution = 'polar')
	A0 = .2
	y = CST(x=x,c=1.,deltasz=[.2,.2],Au=[A0,.8,.2], Al = [.2,3,.4])
	pprint (x)
	pprint (y)

class Window(QtGui.QDialog):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		self.setGeometry(400,50,1200,980)
		self.setWindowTitle('CST control!!!')
		self.setWindowIcon(QtGui.QIcon('images.png'))

		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		btnR = QtGui.QPushButton('Refresh', self)
		btnR.clicked.connect(CSTMOD)

		btnQ = QtGui.QPushButton('Quit', self)
		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)

		self.spDelta = QtGui.QSpinBox(self)
		self.spDelta.setRange(0, 1)
		self.spDelta.setSingleStep(1)

		self.slDelta = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slDelta.setMinimum(0)
		self.slDelta.setMaximum(100)
		self.slDelta.setValue(0)
		self.slDelta.setTickInterval(10)
		self.slDelta.setTickPosition(QtGui.QSlider.TicksBelow)

		self.spAu0 = QtGui.QSpinBox(self)
		self.spAu0.setRange(0, 1)
		self.spAu0.setSingleStep(1)

		self.slAu0 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAu0.setMinimum(0)
		self.slAu0.setMaximum(100)
		self.slAu0.setValue(0)
		self.slAu0.setTickInterval(10)
		self.slAu0.setTickPosition(QtGui.QSlider.TicksBelow)

		self.spAu1 = QtGui.QSpinBox(self)
		self.spAu1.setRange(0, 1)
		self.spAu1.setSingleStep(1)

		self.slAu1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAu1.setMinimum(0)
		self.slAu1.setMaximum(100)
		self.slAu1.setValue(0)
		self.slAu1.setTickInterval(10)
		self.slAu1.setTickPosition(QtGui.QSlider.TicksBelow)

		self.spAl0 = QtGui.QSpinBox(self)
		self.spAl0.setRange(0, 1)
		self.spAl0.setSingleStep(1)

		self.slAl0 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAl0.setMinimum(0)
		self.slAl0.setMaximum(100)
		self.slAl0.setValue(0)
		self.slAl0.setTickInterval(10)
		self.slAl0.setTickPosition(QtGui.QSlider.TicksBelow)

		self.spAl1 = QtGui.QSpinBox(self)
		self.spAl1.setRange(0, 1)
		self.spAl1.setSingleStep(1)

		self.slAl1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAl1.setMinimum(0)
		self.slAl1.setMaximum(100)
		self.slAl1.setValue(0)
		self.slAl1.setTickInterval(10)
		self.slAl1.setTickPosition(QtGui.QSlider.TicksBelow)

		self.slDelta.valueChanged.connect(self.spDelta.setValue)
		self.spDelta.valueChanged.connect(self.slDelta.setValue)

		self.slAu0.valueChanged.connect(self.spAu0.setValue)
		self.spAu0.valueChanged.connect(self.slAu0.setValue)

		self.slAu1.valueChanged.connect(self.spAu1.setValue)
		self.spAu1.valueChanged.connect(self.slAu1.setValue)

		self.slAl0.valueChanged.connect(self.spAl0.setValue)
		self.spAl0.valueChanged.connect(self.slAl0.setValue)

		self.slAl1.valueChanged.connect(self.spAl1.setValue)
		self.spAl1.valueChanged.connect(self.slAl1.setValue)
		
		grid.addWidget(self.spDelta)
		grid.addWidget(self.slDelta)
		grid.addWidget(self.spAu0)
		grid.addWidget(self.slAu0)
		grid.addWidget(self.spAu1)
		grid.addWidget(self.slAu1)
		grid.addWidget(self.spAl0)
		grid.addWidget(self.slAl0)
		grid.addWidget(self.spAl1)
		grid.addWidget(self.slAl1)
		grid.addWidget(btnR)
		grid.addWidget(btnQ)


run()