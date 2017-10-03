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
		grid.addWidget(btnR)

		btnQ = QtGui.QPushButton('Quit', self)
		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)
		grid.addWidget(btnQ)

		self.spAu0 = QtGui.QSpinBox(self)
		self.spAu0.setRange(0, 1)
		self.spAu0.setSingleStep(1)

		self.slAu0 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAu0.setMinimum(0)
		self.slAu0.setMaximum(100)
		self.slAu0.setValue(0)
		self.slAu0.setTickInterval(10)

		self.spAu1 = QtGui.QSpinBox(self)
		self.spAu1.setRange(0, 1)
		self.spAu1.setSingleStep(1)

		self.slAu1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAu1.setMinimum(0)
		self.slAu1.setMaximum(100)
		self.slAu1.setValue(0)
		self.slAu1.setTickInterval(10)

		self.spAl0 = QtGui.QSpinBox(self)
		self.spAl0.setRange(0, 1)
		self.spAl0.setSingleStep(1)

		self.slAl0 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAl0.setMinimum(0)
		self.slAl0.setMaximum(100)
		self.slAl0.setValue(0)
		self.slAl0.setTickInterval(10)

		self.spAl1 = QtGui.QSpinBox(self)
		self.spAl1.setRange(0, 1)
		self.spAl1.setSingleStep(1)

		self.slAl1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAl1.setMinimum(0)
		self.slAl1.setMaximum(100)
		self.slAl1.setValue(0)
		self.slAl1.setTickInterval(10)
		

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