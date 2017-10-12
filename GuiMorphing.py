
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
import inspect

def run():
	app = QtGui.QApplication(sys.argv)
	# n = 4
	n = input("Number of point:\n")
	if n > 6 or n == 1:
		print "Number of point have to be between 2 and 6."
		quit()
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

		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		self.fig = Figure() 
		self.canvas = FigureCanvas(self.fig)

		btnQ = QtGui.QPushButton('Quit', self)
		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)

		def Morphing_Mod():
			attrSLX = 'slDeltaX' + str(1)
			attrSLY = 'slDeltaY' + str(1)

			Xt = float(getattr(self,attrSLX).value())/100
			Yt = float(getattr(self,attrSLY).value())/100

			tip_displacement = {'x':.1 + Xt, 'y':1. + Yt}

			attrSLX = []
			attrSLY = []
			DX = []
			DY = []

			for i in range (n-1):
				attrSLX.append('slDeltaX' + str(i+2))
				attrSLY.append('slDeltaY' + str(i+2))

				DX.append(float((getattr(self,attrSLX[i])).value())/100)
				DY.append(float((getattr(self,attrSLY[i])).value())/100)

			if n >= 2:
				other_points = {'x': [0.01 + DX[0]], 'y': [0.1 + DY[0]]}
			if n >= 3:
				other_points = {'x': [DX[1], .01 + DX[0]], 'y': [0.1 + DY[1], .3 + DY[0]]}
			if n >= 4:
				other_points = {'x': [0.01 + DX[2], -0.03 + DX[1], .05 + DX[0]], 'y': [0.1 + DY[2], 0.3 + DY[1], .5 + DY[0]]}
			if n >= 5:
				other_points = {'x': [0.01 + DX[3], -0.03 + DX[2], .05 + DX[1], 0.12 + DX[0]], 'y': [0.1 + DY[3], 0.3 + DY[2], .5 + DY[1], 0.8 + DY[0]]}
			if n == 6:
				other_points = {'x': [0.01 + DX[4], -0.03 + DX[2], .05 + DX[1], 0.12 + DX[0], 0.01 + DX[3]], 'y': [0.08 + DY[4], 0.3 + DY[2], .5 + DY[1], 0.8 + DY[0], .17 + DY[3]]}

			A0 = -tip_displacement['x']
			A = calculate_shape_coefficients_tracing(A0, tip_displacement, other_points, 1., 1.)
			y = np.linspace(0, tip_displacement['y'], 100000)
			x = CST(y, tip_displacement['y'], deltasz= tip_displacement['x'],  Au = A, N1=1., N2=1.)

			ax = self.fig.add_subplot(111)
			ax.clear()
			ax.plot(x,y)
			ax.scatter(other_points['x'] + [tip_displacement['x']],other_points['y'] + [tip_displacement['y']])
			ax.set_aspect('equal')
			self.canvas.draw()

		btnS = QtGui.QPushButton('Start', self)
		btnS.clicked.connect(Morphing_Mod)

		grid.addWidget(self.canvas)

		for i in range(n):
			attrSPX = 'spDeltaX'+str(i+1)
			setattr(self, attrSPX, QtGui.QSpinBox(self))
			getattr(self,attrSPX).setRange(-50,50)
			getattr(self,attrSPX).setSingleStep(1)

			attrSPY = 'spDeltaY'+str(i+1)
			setattr(self, attrSPY, QtGui.QSpinBox(self))
			getattr(self,attrSPY).setRange(-20,20)
			getattr(self,attrSPY).setSingleStep(1)

			attrSLX = 'slDeltaX'+str(i+1)
			setattr(self, attrSLX, QtGui.QSlider(QtCore.Qt.Horizontal, self))
			getattr(self,attrSLX).setMinimum(-50)
			getattr(self,attrSLX).setMaximum(50)
			getattr(self,attrSLX).setValue(0)
			getattr(self,attrSLX).setTickPosition(QtGui.QSlider.TicksBelow)
			getattr(self,attrSLX).setTickInterval(5)

			attrSLY = 'slDeltaY'+str(i+1)
			setattr(self, attrSLY, QtGui.QSlider(QtCore.Qt.Vertical, self))
			getattr(self,attrSLY).setMinimum(-20)
			getattr(self,attrSLY).setMaximum(20)
			getattr(self,attrSLY).setValue(0)
			getattr(self,attrSLY).setTickPosition(QtGui.QSlider.TicksBelow)
			getattr(self,attrSLY).setTickInterval(5)

			grid.addWidget(getattr(self,attrSPX),i+2,2)
			grid.addWidget(getattr(self,attrSLX),i+2,0)

			grid.addWidget(getattr(self,attrSPY),i+2,3)
			grid.addWidget(getattr(self,attrSLY),i+2,1)

			getattr(self,attrSLX).valueChanged.connect(getattr(self,attrSPX).setValue)
			getattr(self,attrSPX).valueChanged.connect(getattr(self,attrSLX).setValue)

			getattr(self,attrSLY).valueChanged.connect(getattr(self,attrSPY).setValue)
			getattr(self,attrSPY).valueChanged.connect(getattr(self,attrSLY).setValue)

			getattr(self,attrSLX).valueChanged.connect(Morphing_Mod)
			getattr(self,attrSLY).valueChanged.connect(Morphing_Mod)

		LabelX= QtGui.QLabel("     X:")
		LabelY= QtGui.QLabel("     Y:")

		grid.addWidget(LabelX,1,2)
		grid.addWidget(LabelY,1,3)

		grid.addWidget(btnS)
		grid.addWidget(btnQ)
run()