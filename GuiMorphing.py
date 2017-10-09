
"Programmed by Antoine BALDO"

from morphing import calculate_shape_coefficients_tracing
from airfoil_module import CST
from CST_module import *
import sys
import os 
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import math
import numpy as np
from PyQt4 import QtGui, QtCore

def run():
	app = QtGui.QApplication(sys.argv)
	# n = input("Number of points:\n")
	# if n > 6:
	# 	print "Number of points have to be between 1 and 6."
	# 	quit()
	n = 5
	GUI = Window(n)
	GUI.show()
	sys.exit(app.exec_())
	QtCore.QCoreApplication.instance().quit

class Window(QtGui.QDialog):
	def __init__(self, n, parent=None):
		super(Window, self).__init__(parent)
		_fromUtf8 = QtCore.QString.fromUtf8
		self.setGeometry(400,40,1200,980)
		self.setWindowTitle('Morphing Control')
		self.setWindowIcon(QtGui.QIcon('images.png'))

		def Morphing_Mod():
			N1 = 1.
	        N2 = 1.
	        tip_displacement = {'x': .1, 'y':1.}
	        other_points = {'x': [0.01, -0.03, .05, 0.12], 'y':[0.1, 0.3, .5, 0.8]}
	        A0 = -tip_displacement['x']
	        # print A0
	        A = calculate_shape_coefficients_tracing(A0, tip_displacement, other_points, 1., 1.)
	        y = np.linspace(0, tip_displacement['y'], 100000)
	        x = CST(y, tip_displacement['y'], deltasz= tip_displacement['x'],  Au = A, N1=1., N2=1.)
	        # plt.plot(x,y)
	        # plt.scatter(other_points['x'] + [tip_displacement['x']], 
	        #             other_points['y'] + [tip_displacement['y']])
	        # plt.gca().set_aspect('equal', adjustable='box')
	        # plt.show()


		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		self.fig = Figure() 
		self.canvas = FigureCanvas(self.fig)

		btnQ = QtGui.QPushButton('Start', self)
		btnQ.clicked.connect(Morphing_Mod)

		grid.addWidget(self.canvas)
######################################################################################################################################################
		if n >= 1:
			Labelx = QtGui.QLabel("     X:")
			self.spDeltaX1 = QtGui.QSpinBox(self)
			self.spDeltaX1.setRange(-100, 100)
			self.spDeltaX1.setSingleStep(1)

			self.slDeltaX1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
			self.slDeltaX1.setMinimum(-100)
			self.slDeltaX1.setMaximum(100)
			self.slDeltaX1.setValue(0)
			self.slDeltaX1.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaX1.setTickInterval(10)

			Labely = QtGui.QLabel("     Y:")
			self.spDeltaY1 = QtGui.QSpinBox(self)
			self.spDeltaY1.setRange(-100, 100)
			self.spDeltaY1.setSingleStep(1)

			self.slDeltaY1 = QtGui.QSlider(QtCore.Qt.Vertical, self)
			self.slDeltaY1.setMinimum(-100)
			self.slDeltaY1.setMaximum(100)
			self.slDeltaY1.setValue(0)
			self.slDeltaY1.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaY1.setTickInterval(10)

			grid.addWidget(Labelx,1,2)
			grid.addWidget(Labely,1,3)

			grid.addWidget(self.spDeltaX1, 2,2)
			grid.addWidget(self.slDeltaX1,2,0)

			grid.addWidget(self.spDeltaY1,2,3)
			grid.addWidget(self.slDeltaY1,2,1)

			self.slDeltaX1.valueChanged.connect(self.spDeltaX1.setValue)
			self.spDeltaX1.valueChanged.connect(self.slDeltaX1.setValue)

			self.slDeltaY1.valueChanged.connect(self.spDeltaY1.setValue)
			self.spDeltaY1.valueChanged.connect(self.slDeltaY1.setValue)
######################################################################################################################################################
		if n >= 2:
			self.spDeltaX2 = QtGui.QSpinBox(self)
			self.spDeltaX2.setRange(-100, 100)
			self.spDeltaX2.setSingleStep(1)

			self.slDeltaX2 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
			self.slDeltaX2.setMinimum(-100)
			self.slDeltaX2.setMaximum(100)
			self.slDeltaX2.setValue(0)
			self.slDeltaX2.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaX2.setTickInterval(10)

			self.spDeltaY2 = QtGui.QSpinBox(self)
			self.spDeltaY2.setRange(-100, 100)
			self.spDeltaY2.setSingleStep(1)

			self.slDeltaY2 = QtGui.QSlider(QtCore.Qt.Vertical, self)
			self.slDeltaY2.setMinimum(-100)
			self.slDeltaY2.setMaximum(100)
			self.slDeltaY2.setValue(0)
			self.slDeltaX2.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaX2.setTickInterval(10)

			grid.addWidget(self.spDeltaX2,3,2)
			grid.addWidget(self.slDeltaX2,3,0)
			
			grid.addWidget(self.spDeltaY2,3,3)
			grid.addWidget(self.slDeltaY2,3,1)

			self.slDeltaX2.valueChanged.connect(self.spDeltaX2.setValue)
			self.spDeltaX2.valueChanged.connect(self.slDeltaX2.setValue)

			self.slDeltaY2.valueChanged.connect(self.spDeltaY2.setValue)
			self.spDeltaY2.valueChanged.connect(self.slDeltaY2.setValue)
######################################################################################################################################################
		if n >= 3:
			self.spDeltaX3 = QtGui.QSpinBox(self)
			self.spDeltaX3.setRange(-100, 100)
			self.spDeltaX3.setSingleStep(1)

			self.slDeltaX3 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
			self.slDeltaX3.setMinimum(-100)
			self.slDeltaX3.setMaximum(100)
			self.slDeltaX3.setValue(0)
			self.slDeltaX3.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaX3.setTickInterval(10)

			self.spDeltaY3 = QtGui.QSpinBox(self)
			self.spDeltaY3.setRange(-100, 100)
			self.spDeltaY3.setSingleStep(1)

			self.slDeltaY3 = QtGui.QSlider(QtCore.Qt.Vertical, self)
			self.slDeltaY3.setMinimum(-100)
			self.slDeltaY3.setMaximum(100)
			self.slDeltaY3.setValue(0)
			self.slDeltaY3.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaY3.setTickInterval(10)

			grid.addWidget(self.spDeltaX3,4,2)
			grid.addWidget(self.slDeltaX3,4,0)
			
			grid.addWidget(self.spDeltaY3,4,3)
			grid.addWidget(self.slDeltaY3,4,1)

			self.slDeltaX3.valueChanged.connect(self.spDeltaX3.setValue)
			self.spDeltaX3.valueChanged.connect(self.slDeltaX3.setValue)

			self.slDeltaY3.valueChanged.connect(self.spDeltaY3.setValue)
			self.spDeltaY3.valueChanged.connect(self.slDeltaY3.setValue)
######################################################################################################################################################
		if n >= 4:
			self.spDeltaX4 = QtGui.QSpinBox(self)
			self.spDeltaX4.setRange(-100, 100)
			self.spDeltaX4.setSingleStep(1)

			self.slDeltaX4 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
			self.slDeltaX4.setMinimum(-100)
			self.slDeltaX4.setMaximum(100)
			self.slDeltaX4.setValue(0)
			self.slDeltaX4.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaX4.setTickInterval(10)

			self.spDeltaY4 = QtGui.QSpinBox(self)
			self.spDeltaY4.setRange(-100, 100)
			self.spDeltaY4.setSingleStep(1)

			self.slDeltaY4 = QtGui.QSlider(QtCore.Qt.Vertical, self)
			self.slDeltaY4.setMinimum(-100)
			self.slDeltaY4.setMaximum(100)
			self.slDeltaY4.setValue(0)
			self.slDeltaY4.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaY4.setTickInterval(10)

			grid.addWidget(self.spDeltaX4,5,2)
			grid.addWidget(self.slDeltaX4,5,0)
			
			grid.addWidget(self.spDeltaY4,5,3)
			grid.addWidget(self.slDeltaY4,5,1)

			self.slDeltaX4.valueChanged.connect(self.spDeltaX4.setValue)
			self.spDeltaX4.valueChanged.connect(self.slDeltaX4.setValue)

			self.slDeltaY4.valueChanged.connect(self.spDeltaY4.setValue)
			self.spDeltaY4.valueChanged.connect(self.slDeltaY4.setValue)
######################################################################################################################################################
		if n >= 5:
			self.spDeltaX5 = QtGui.QSpinBox(self)
			self.spDeltaX5.setRange(-100, 100)
			self.spDeltaX5.setSingleStep(1)

			self.slDeltaX5 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
			self.slDeltaX5.setMinimum(-100)
			self.slDeltaX5.setMaximum(100)
			self.slDeltaX5.setValue(0)
			self.slDeltaX5.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaX5.setTickInterval(10)

			self.spDeltaY5 = QtGui.QSpinBox(self)
			self.spDeltaY5.setRange(-100, 100)
			self.spDeltaY5.setSingleStep(1)

			self.slDeltaY5 = QtGui.QSlider(QtCore.Qt.Vertical, self)
			self.slDeltaY5.setMinimum(-100)
			self.slDeltaY5.setMaximum(100)
			self.slDeltaY5.setValue(0)
			self.slDeltaY5.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaY5.setTickInterval(10)

			grid.addWidget(self.spDeltaX5,6,2)
			grid.addWidget(self.slDeltaX5,6,0)
			
			grid.addWidget(self.spDeltaY5,6,3)
			grid.addWidget(self.slDeltaY5,6,1)

			self.slDeltaX5.valueChanged.connect(self.spDeltaX5.setValue)
			self.spDeltaX5.valueChanged.connect(self.slDeltaX5.setValue)

			self.slDeltaY5.valueChanged.connect(self.spDeltaY5.setValue)
			self.spDeltaY5.valueChanged.connect(self.slDeltaY5.setValue)
######################################################################################################################################################
		if n == 6:
			self.spDeltaX6 = QtGui.QSpinBox(self)
			self.spDeltaX6.setRange(-100, 100)
			self.spDeltaX6.setSingleStep(1)

			self.slDeltaX6 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
			self.slDeltaX6.setMinimum(-100)
			self.slDeltaX6.setMaximum(100)
			self.slDeltaX6.setValue(0)
			self.slDeltaX6.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaX6.setTickInterval(10)

			self.spDeltaY6 = QtGui.QSpinBox(self)
			self.spDeltaY6.setRange(-100, 100)
			self.spDeltaY6.setSingleStep(1)

			self.slDeltaY6 = QtGui.QSlider(QtCore.Qt.Vertical, self)
			self.slDeltaY6.setMinimum(-100)
			self.slDeltaY6.setMaximum(100)
			self.slDeltaY6.setValue(0)
			self.slDeltaY6.setTickPosition(QtGui.QSlider.TicksBelow)
			self.slDeltaY6.setTickInterval(10)

			grid.addWidget(self.spDeltaX6,7,2)
			grid.addWidget(self.slDeltaX6,7,0)
			
			grid.addWidget(self.spDeltaY6,7,3)
			grid.addWidget(self.slDeltaY6,7,1)

			self.slDeltaX6.valueChanged.connect(self.spDeltaX6.setValue)
			self.spDeltaX6.valueChanged.connect(self.slDeltaX6.setValue)

			self.slDeltaY6.valueChanged.connect(self.spDeltaY6.setValue)
			self.spDeltaY6.valueChanged.connect(self.slDeltaY6.setValue)

######################################################################################################################################################
		grid.addWidget(btnQ)

run()