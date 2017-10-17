
"Programmed by Antoine BALDO"

from morphing import calculate_dependent_shape_coefficients
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
	GUI = Window()
	GUI.show()
	sys.exit(app.exec_())

class Window(QtGui.QDialog):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		_fromUtf8 = QtCore.QString.fromUtf8
		self.setGeometry(100,50,1200,650)
		self.setWindowTitle('Structurally Consistent Control')
		self.setWindowIcon(QtGui.QIcon('images.png'))

		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		self.fig = Figure() 
		self.canvas = FigureCanvas(self.fig)

		btnQ = QtGui.QPushButton('Quit', self)
		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)

		def structurally_consistent():
			morphing_direction = 'forwards'
			c_P = 1.
			deltaz = 0.*c_P

			Au_P =  [0.10887, 0.1187, 0.07843, 0.12084, 0.07919, 0.09840]
			Al_P =  [0.11117, 0.1000, 0.1239, 0.06334, 0.11539, 0.10400]
			n = len(Au_P) - 1

			attrSPACu = []
			attrSPpsispar = []
			V_AC_u = []
			V_psi_spar = []

			for i in range (1,6):
				attrSLACu.append('spAC_u' + str(i))
				attrSLpsispar.append('sppsi_spar' + str(i))

				V_AC_u.append(float((getattr(self,attrSLACu[i])).value())/10000)
				V_psi_spar.append(float((getattr(self,attrSLpsispar[i])).value())/10)

			AC_u1 = V_AC_u[1]
			AC_u2 = V_AC_u[2]
			AC_u3 = V_AC_u[3]
			AC_u4 = V_AC_u[4]
			AC_u5 = V_AC_u[5]

			psi_spar1 = V_psi_spar[1]
			psi_spar2 = V_psi_spar[2]
			psi_spar3 = V_psi_spar[3]
			psi_spar4 = V_psi_spar[4]
			psi_spar5 = V_psi_spar[5]
			psi_spars = [psi_spar1, psi_spar2, psi_spar3, psi_spar4, psi_spar5]

			Au_C, Al_C, c_C, spar_thicknesses = calculate_dependent_shape_coefficients(
	                                                            AC_u1, AC_u2, AC_u3, AC_u4, AC_u5,
	                                                            psi_spars, Au_P, Al_P,
	                                                            deltaz, c_P, morphing=morphing_direction)
			np.set_printoptions(precision=20)

			ax = self.fig.add_subplot(111)
			ax.clear()

			# Print shape for children
			x = np.linspace(0, c_C, 100000)
			y = CST(x, c_C, deltasz= [deltaz/2., deltaz/2.],  Al= Al_C, Au =Au_C)
			ax.plot(x, y['u'],'r',label = 'Children', lw=2)
			ax.plot(x, y['l'],'r',label = None, lw=2)

			# Print shape for parent
			x = np.linspace(0, c_P, 100000)
			y = CST(x, c_P, deltasz= [deltaz/2., deltaz/2.],  Al= Al_P, Au =Au_P)
			ax.plot(x, y['u'],'b',label='Parent', lw=2)
			ax.plot(x, y['l'],'b',label = None, lw=2)
			self.canvas.draw()


		btnR = QtGui.QPushButton('Refresh', self)
		btnR.clicked.connect(structurally_consistent)

		grid.addWidget(self.canvas)

		for i in range (1,6):
			attrSPACu = 'spAC_u'+str(i)
			setattr(self, attrSPACu, QtGui.QSpinBox(self))
			getattr(self,attrSPACu).setRange(0,10000)
			getattr(self,attrSPACu).setSingleStep(1)

			attrSPpsispar = 'sppsi_spar'+str(i)
			setattr(self, attrSPpsispar, QtGui.QSpinBox(self))
			getattr(self,attrSPpsispar).setRange(0,10)
			getattr(self,attrSPpsispar).setSingleStep(1)

			grid.addWidget(getattr(self,attrSPACu),i,0)
			grid.addWidget(getattr(self,attrSPpsispar),i,1)

		grid.addWidget(btnR)
		grid.addWidget(btnQ)


run()