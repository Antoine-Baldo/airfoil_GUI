
"Programmed by Antoine BALDO"

from morphing import calculate_shape_coefficients_tracing
from airfoil_module import CST
from CST_module import *
import sys
import os 
from pprint import pprint
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import math
import numpy as np
from PyQt4 import QtGui, QtCore

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
		self.setGeometry(200,35,1000,750)
		self.setWindowTitle('Morphing Control')
		self.setWindowIcon(QtGui.QIcon('images.png'))

		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		self.fig = Figure() 
		self.canvas = FigureCanvas(self.fig)

		btnQ = QtGui.QPushButton('Quit', self)
		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)

		def Morphing_Mod():
			attrSPX = []
			attrSPY = []
			X = []
			Y = []
			ax = self.fig.add_subplot(111)
			ax.clear()

			for i in range (n):
				attrSPX.append('spX' + str(i+1))
				attrSPY.append('spY' + str(i+1))

				X.append(float((getattr(self,attrSPX[i])).value())/100)
				Y.append(float((getattr(self,attrSPY[i])).value())/100)

			tip_displacement = {'x':0.1+X[0], 'y':1+Y[0]}

			if n >= 2:
				other_points = {'x': [0.01 + X[1]], 'y': [0.1 + Y[1]]}
			if n >= 3:
				other_points = {'x': [X[2]+0.05, .01 + X[1]], 'y': [0.1 + Y[2], .3 + Y[1]]}
			if n >= 4:
				other_points = {'x': [0.01 + X[3], -0.03 + X[2], .05 + X[1]], 'y': [0.1 + Y[3], 0.3 + Y[2], .5 + Y[1]]}
			if n >= 5:
				other_points = {'x': [0.01 + X[4], -0.03 + X[3], .05 + X[2], 0.12 + X[1]], 
				                'y': [0.1 + Y[4], 0.3 + Y[3], .5 + Y[2], 0.8 + Y[1]]}
			if n == 6:
				other_points = {'x': [0.01 + X[5], -0.03 + X[3], .05 + X[2], 0.12 + X[1], 0.01 + X[4]], 
				                'y': [0.08 + Y[5], 0.3 + Y[3], .5 + Y[2], 0.8 + Y[1], .17 + Y[4]]}

			A0 = -tip_displacement['x']
			A = calculate_shape_coefficients_tracing(A0, other_points['y'], other_points['x'], 1., 1., chord = tip_displacement['y'], EndThickness = tip_displacement['x'])

			#plotting
			y = np.linspace(0, tip_displacement['y'], 100000)
			x = CST(y, tip_displacement['y'], deltasz= tip_displacement['x'],  Au = A, N1=1., N2=1.)
			ax.plot(x,y)
			ax.scatter(other_points['x'] + [tip_displacement['x']], 
			            other_points['y'] + [tip_displacement['y']])

			ax.set_aspect('equal')
			ax.set_ylim([0,1.1])
			ax.set_xlim([-1.5,1.5])
			self.canvas.draw()

		btnS = QtGui.QPushButton('Start', self)
		btnS.clicked.connect(Morphing_Mod)

		grid.addWidget(self.canvas)

		for i in range(n):
			attrSPX = 'spX'+str(i+1)
			setattr(self, attrSPX, QtGui.QSpinBox(self))
			getattr(self,attrSPX).setRange(-50,50)
			getattr(self,attrSPX).setSingleStep(1)
			
			attrSPY = 'spY'+str(i+1)
			setattr(self, attrSPY, QtGui.QSpinBox(self))
			getattr(self,attrSPY).setRange(-50,50)
			getattr(self,attrSPY).setSingleStep(1)

			attrSLX = 'slX'+str(i+1)
			setattr(self, attrSLX, QtGui.QSlider(QtCore.Qt.Horizontal, self))
			getattr(self,attrSLX).setMinimum(-50)
			getattr(self,attrSLX).setMaximum(50)
			getattr(self,attrSLX).setTickPosition(QtGui.QSlider.TicksBelow)
			getattr(self,attrSLX).setTickInterval(10)

			attrSLY = 'slY'+str(i+1)
			setattr(self, attrSLY, QtGui.QSlider(QtCore.Qt.Vertical, self))
			getattr(self,attrSLY).setMinimum(-25)
			getattr(self,attrSLY).setMaximum(25)
			getattr(self,attrSLY).setTickPosition(QtGui.QSlider.TicksBelow)
			getattr(self,attrSLY).setTickInterval(10)

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