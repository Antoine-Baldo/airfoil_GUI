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

# https://stackoverflow.com/questions/20632841/qt-horizontalslider-send-float-values

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	GUI.show()
	sys.exit(app.exec_())

class Window(QtGui.QDialog):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		_fromUtf8 = QtCore.QString.fromUtf8
		self.setGeometry(400,50,1200,980)
		self.setWindowTitle('CST Control')
		self.setWindowIcon(QtGui.QIcon('images.png'))

		def CSTMOD():
			chord = 1.
			n = 200
			x = create_x(chord, n, distribution = 'polar')
			ax = self.fig.add_subplot(111)

			V_Au0 = self.slAu0.value()
			V_Au1 = self.slAu1.value()
			V_Al0 = self.slAl0.value()
			V_Al1 = self.slAl1.value()
			V_Deltasz = self.slDelta.value()

			# V_Au0 = 15
			# V_Au1 = 20
			# V_Al0 = 22
			# V_Al1 = 9
			# V_Deltasz = 30

			Au0 = (float(V_Au0)/100)
			Au1 = (float(V_Au1)/100)
			Al0 = (float(V_Al0)/100)
			Al1 = (float(V_Al1)/100)
			Deltasz = (float(V_Deltasz)/1000)

			cst = CST(x = x,c = 1.,deltasz = [Deltasz, Deltasz],Au = [Au0, Au1], Al = [Al0,Al1])

			print 'cst:'
			pprint (cst)

			data1 = [float(cst['l'][k]) for k in range(n)]
			data2 = [float(cst['u'][k]) for k in range(n)]
			
			ax.clear()
			ax.plot(data1, data2, '*-')
			self.canvas.draw()

		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		self.fig = Figure() 
		self.canvas = FigureCanvas(self.fig)

		btnR = QtGui.QPushButton('Refresh', self)
		btnR.clicked.connect(CSTMOD)

		btnQ = QtGui.QPushButton('Quit', self)
		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)

		LabelDelta = QtGui.QLabel("Deltasz (x0.001):")

		self.spDelta = QtGui.QSpinBox(self)
		self.spDelta.setRange(0, 100)
		self.spDelta.setSingleStep(1)

		self.slDelta = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slDelta.setMinimum(0)
		self.slDelta.setMaximum(150)
		self.slDelta.setValue(0)
		self.slDelta.setTickPosition(QtGui.QSlider.TicksBelow)
		self.slDelta.setTickInterval(10)

		LabelAu0 = QtGui.QLabel("Au0 (x0.01):")

		self.spAu0 = QtGui.QSpinBox(self)
		self.spAu0.setRange(0, 100)
		self.spAu0.setSingleStep(1)

		self.slAu0 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAu0.setMinimum(0)
		self.slAu0.setMaximum(100)
		self.slAu0.setValue(0)
		self.slAu0.setTickInterval(10)
		self.slAu0.setTickPosition(QtGui.QSlider.TicksBelow)

		LabelAu1 = QtGui.QLabel("Au1 (x0.01):")

		self.spAu1 = QtGui.QSpinBox(self)
		self.spAu1.setRange(0, 100)
		self.spAu1.setSingleStep(1)

		self.slAu1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAu1.setMinimum(0)
		self.slAu1.setMaximum(100)
		self.slAu1.setValue(0)
		self.slAu1.setTickInterval(10)
		self.slAu1.setTickPosition(QtGui.QSlider.TicksBelow)

		LabelAl0 = QtGui.QLabel("Al0 (x0.01):")

		self.spAl0 = QtGui.QSpinBox(self)
		self.spAl0.setRange(0, 100)
		self.spAl0.setSingleStep(1)

		self.slAl0 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAl0.setMinimum(0)
		self.slAl0.setMaximum(100)
		self.slAl0.setValue(0)
		self.slAl0.setTickInterval(10)
		self.slAl0.setTickPosition(QtGui.QSlider.TicksBelow)

		LabelAl1 = QtGui.QLabel("Al1 (x0.01):")

		self.spAl1 = QtGui.QSpinBox(self)
		self.spAl1.setRange(0, 100)
		self.spAl1.setSingleStep(1)

		self.slAl1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slAl1.setMinimum(0)
		self.slAl1.setMaximum(100)
		self.slAl1.setValue(0)
		self.slAl1.setTickInterval(10)
		self.slAl1.setTickPosition(QtGui.QSlider.TicksBelow)

		self.toolbar = NavigationToolbar(self.canvas, self)

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

		grid.addWidget(self.canvas)
		grid.addWidget(LabelDelta)
		grid.addWidget(self.spDelta)
		grid.addWidget(self.slDelta)
		grid.addWidget(LabelAu0)
		grid.addWidget(self.spAu0)
		grid.addWidget(self.slAu0)
		grid.addWidget(LabelAu1)
		grid.addWidget(self.spAu1)
		grid.addWidget(self.slAu1)
		grid.addWidget(LabelAl0)
		grid.addWidget(self.spAl0)
		grid.addWidget(self.slAl0)
		grid.addWidget(LabelAl1)
		grid.addWidget(self.spAl1)
		grid.addWidget(self.slAl1)
		grid.addWidget(btnR)
		grid.addWidget(btnQ)
		grid.addWidget(self.toolbar)

run()