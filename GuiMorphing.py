
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
	# n = 5
	n = input("Number of points:\n")
	if n > 6 or n == 1:
		print "Number of points have to be between 2 and 6."
		quit()
	GUI = Window(n)
	import inspect
	a = inspect.getmembers(GUI)
	print len(a), type(a), type(a[0][0]), a[0][0]
	for i in range(len(a)):
		if a[i][0][0] == 's':
			print a[i][0]
	BREAK
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
			tip_displacement = {'x': .1, 'y':1.}

			if n-1 >= 1:
				DeltaX1 = float(self.slDeltaX1.value())/100
				DeltaY1 = float(self.slDeltaY1.value())/100

				other_points = {'x': [0.01 + DeltaX1], 'y':[0.1 + DeltaY1]}
				A0 = -tip_displacement['x']
				# print A0
				A = calculate_shape_coefficients_tracing(A0, tip_displacement, other_points, 1., 1.)
				y = np.linspace(0, tip_displacement['y'], 100000)
				x = CST(y, tip_displacement['y'], deltasz= tip_displacement['x'],  Au = A, N1=1., N2=1.)

			if n-1 >= 2:
				DeltaX2 = float(self.slDeltaX2.value())/100
				DeltaY2 = float(self.slDeltaY2.value())/100

				other_points = {'x': [0.01 + DeltaX2, -0.03 + DeltaX1], 'y':[0.1 + DeltaY2, 0.3 + DeltaY1]}
				A0 = -tip_displacement['x']
				# print A0
				A = calculate_shape_coefficients_tracing(A0, tip_displacement, other_points, 1., 1.)
				y = np.linspace(0, tip_displacement['y'], 100000)
				x = CST(y, tip_displacement['y'], deltasz= tip_displacement['x'],  Au = A, N1=1., N2=1.)

			if n-1 >= 3:
				DeltaX3 = float(self.slDeltaX3.value())/100
				DeltaY3 = float(self.slDeltaY3.value())/100

				other_points = {'x': [0.01 + DeltaX3, -0.03 + DeltaX2, .05 + DeltaX1], 'y':[0.1 + DeltaY3, 0.3 + DeltaY2, .5 + DeltaY1]}
				A0 = -tip_displacement['x']
				# print A0
				A = calculate_shape_coefficients_tracing(A0, tip_displacement, other_points, 1., 1.)
				y = np.linspace(0, tip_displacement['y'], 100000)
				x = CST(y, tip_displacement['y'], deltasz= tip_displacement['x'],  Au = A, N1=1., N2=1.)

			if n-1 >= 4:
				DeltaX4 = float(self.slDeltaX4.value())/100
				DeltaY4 = float(self.slDeltaY4.value())/100

				other_points = {'x': [0.01 + DeltaX4, -0.03 + DeltaX3, .05 + DeltaX2, 0.12 + DeltaX1], 'y':[0.1 + DeltaY4, 0.3 + DeltaY3, .5 + DeltaY2, 0.8 + DeltaY1]}
				A0 = -tip_displacement['x']
				# print A0
				A = calculate_shape_coefficients_tracing(A0, tip_displacement, other_points, 1., 1.)
				y = np.linspace(0, tip_displacement['y'], 100000)
				x = CST(y, tip_displacement['y'], deltasz= tip_displacement['x'],  Au = A, N1=1., N2=1.)
				
			if n-1 >= 5:
				DeltaX5 = float(self.slDeltaX5.value())/100
				DeltaY5 = float(self.slDeltaY5.value())/100

				other_points = {'x': [0.01 + DeltaX5, -0.03 + DeltaX3, .05 + DeltaX2, 0.12 + DeltaX1, 0.01 + DeltaX4], 'y':[0.1 + DeltaY5, 0.3 + DeltaY3, .5 + DeltaY2, 0.8 + DeltaY1, .17 + DeltaY4]}
				A0 = -tip_displacement['x']
				# print A0
				A = calculate_shape_coefficients_tracing(A0, tip_displacement, other_points, 1., 1.)
				y = np.linspace(0, tip_displacement['y'], 100000)
				x = CST(y, tip_displacement['y'], deltasz= tip_displacement['x'],  Au = A, N1=1., N2=1.)

			ax = self.fig.add_subplot(111)
			ax.clear()
			ax.plot(x,y)
			ax.scatter(other_points['x'] + [tip_displacement['x']], 
						other_points['y'] + [tip_displacement['y']])
			ax.set_aspect('equal')
			self.canvas.draw()

		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		self.fig = Figure() 
		self.canvas = FigureCanvas(self.fig)

		btnQ = QtGui.QPushButton('Quit', self)
		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)

		btnS = QtGui.QPushButton('Start', self)
		btnS.clicked.connect(Morphing_Mod)

		grid.addWidget(self.canvas)
######################################################################################################################################################
		if n-1 >= 1:
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

			self.slDeltaX1.valueChanged.connect(Morphing_Mod)
			self.slDeltaY1.valueChanged.connect(Morphing_Mod)
######################################################################################################################################################
		if n-1 >= 2:
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

			self.slDeltaX2.valueChanged.connect(Morphing_Mod)
			self.slDeltaY2.valueChanged.connect(Morphing_Mod)
######################################################################################################################################################
		if n-1 >= 3:
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

			self.slDeltaX3.valueChanged.connect(Morphing_Mod)
			self.slDeltaY3.valueChanged.connect(Morphing_Mod)
######################################################################################################################################################
		if n-1 >= 4:
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

			self.slDeltaX4.valueChanged.connect(Morphing_Mod)
			self.slDeltaY4.valueChanged.connect(Morphing_Mod)
######################################################################################################################################################
		if n-1 >= 5:
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

			self.slDeltaX5.valueChanged.connect(Morphing_Mod)
			self.slDeltaY5.valueChanged.connect(Morphing_Mod)
######################################################################################################################################################
		grid.addWidget(btnS)
		grid.addWidget(btnQ)

run()