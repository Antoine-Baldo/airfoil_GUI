from morphing import calculate_shape_coefficients_tracing, calculate_dependent_shape_coefficients
from airfoil_module import CST
from CST_module import *
import sys
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt4 import QtGui, QtCore

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	GUI.show()
	sys.exit(app.exec_())

class Window(QtGui.QDialog):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		_fromUtf8 = QtCore.QString.fromUtf8
		self.setGeometry(200,50,1100,650)
		self.setWindowTitle('Ultimate Morphing Control Module')
		self.setWindowIcon(QtGui.QIcon('images.png'))
		grid = QtGui.QGridLayout()
		self.setLayout(grid)
		self.fig = Figure() 
		self.canvas = FigureCanvas(self.fig)
		btnQ = QtGui.QPushButton('Quit', self)
		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)

		def Morphing():
			morphing_direction = 'forwards'
			inverted = False

			# Points where children should be
			# ValX = [0.1 ,0.25,0.42,0.65,.9]
			# ValY = [0.02,0.03,0.04,0.05,.05]

			attrSPX = []
			attrSPY = []
			ValX = []
			ValY = []

			for i in range (5):
				attrSPX.append('spX' + str(i+1))
				attrSPY.append('spY' + str(i+1))

				ValX.append(float((getattr(self,attrSPX[i])).value())/100)
				ValY.append(float((getattr(self,attrSPY[i])).value())/100)
			print "ValX:", ValX
			print "ValY:", ValY

			# Geoemtric propeties for parent
			c_P = 1.
			Au_P =  [0.10887, 0.1187, 0.07843, 0.12084, 0.07919, 0.09840]
			Al_P =  [0.11117, 0.1000, 0.1239, 0.06334, 0.11539, 0.10400]
			psi_spars = [0.2,0.3,0.5,0.7,0.9]
			deltaz = 0

			# Initialize values before iteration
			AC_u0 = Au_P[0]
			c_C = c_P

			# Initialize the Figure
			ax = self.fig.add_subplot(111)
			ax.clear()

			# Iterative method is necessary because the value of Au_C is not known
			tol = 1e-6
			error = 99999.
			counter = 1
			while error>tol:
			    # tracing :
			    A = calculate_shape_coefficients_tracing(AC_u0, ValX, ValY, 0.5, 1.,c_C, deltaz)
			    # structurally_consistent :
			    Au_C, Al_C, c_C, spar_thicknesses = calculate_dependent_shape_coefficients(
			                                                        A[1:], psi_spars, Au_P, Al_P,
			                                                        deltaz, c_P, morphing=morphing_direction)
			    error = abs((AC_u0-Au_C[0])/AC_u0) 
			    print 'Iteration: ' + str(counter) + ', Error: ' +str(error)
			    AC_u0 = Au_C[0]
			    counter += 1

			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			# Plotting :
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			x = np.linspace(0, c_C, 1000)
			y = CST(x, c_C, deltasz= [deltaz/2., deltaz/2.],  Al= Al_C, Au =Au_C)
			ax.plot(x, y['u'],'b',label = 'Children', lw=2)
			ax.plot(x, y['l'],'b',label = None, lw=2)

			# Print shape for parent
			x = np.linspace(0, c_P, 1000)
			y = CST(x, c_P, deltasz= [deltaz/2., deltaz/2.],  Al= Al_P, Au =Au_P)
			ax.plot(x, y['u'],'r--',label='Parent', lw=2)
			ax.plot(x, y['l'],'r--',label = None, lw=2)

			if morphing_direction == 'forwards':
				psi_flats = []
				intersections_x_children = [0]
				intersections_y_children = [0]
				intersections_x_parent = [0]
				intersections_y_parent = [0]
				for j in range(len(psi_spars)):
					psi_parent_j = psi_spars[j]
					# Calculate psi at landing
					# psi_baseline, Au_baseline, Au_goal, deltaz, c_baseline, c_goal
					psi_children_j = calculate_psi_goal(psi_parent_j, Au_P, Au_C, deltaz, c_P, c_C)
					x_children_j = psi_children_j*c_C

					# Calculate xi at landing
					temp = CST(x_children_j, c_C, [deltaz/2., deltaz/2.], Al= Al_C, Au =Au_C)
					y_children_j = temp['u']

					s = calculate_spar_direction(psi_spars[j], Au_P, Au_C, deltaz, c_C)

					# Print spars for children
					ax.plot([x_children_j, x_children_j - spar_thicknesses[j]*s[0]],[y_children_j, y_children_j - spar_thicknesses[j]*s[1]], c = 'b', lw=2, label=None)
					psi_flats.append(x_children_j - spar_thicknesses[j]*s[0])
					y = CST(np.array([psi_parent_j*c_P]), c_P, deltasz=[deltaz/2., deltaz/2.], Al= Al_P, Au =Au_P)

					intersections_x_children.append(x_children_j - spar_thicknesses[j]*s[0])
					intersections_y_children.append(y_children_j - spar_thicknesses[j]*s[1])

					# Print spars for parents
					ax.plot([psi_parent_j*c_P, psi_parent_j*c_P], [y['u'], y['u']-spar_thicknesses[j]], 'r--', lw=2, label = None)

					intersections_x_parent.append(psi_parent_j*c_P)
					intersections_y_parent.append(y['u']-spar_thicknesses[j])

			ax.scatter([0]+ValX, [0]+ValY)
			ax.set_xlabel('$\psi^p$', fontsize = 14)
			ax.set_ylabel(r'$\xi^p$', fontsize = 14)
			ax.set_ylim([-0.06,0.17])
			ax.grid()
			ax.set_aspect('equal', adjustable='box')
			ax.legend(loc=1)
			self.canvas.draw()

		btnS = QtGui.QPushButton('Start', self)
		btnS.clicked.connect(Morphing)

		grid.addWidget(self.canvas,0,0,1,-1)

		X = [10 ,25,42,65,90]
		Y = [2,3,4,5,5]

		for i in range(5):
			attrSPX = 'spX'+str(i+1)
			setattr(self, attrSPX, QtGui.QSpinBox(self))
			getattr(self,attrSPX).setRange(-150,150)
			getattr(self,attrSPX).setSingleStep(1)
			getattr(self,attrSPX).setValue(X[i])

			attrSPY = 'spY'+str(i+1)
			setattr(self, attrSPY, QtGui.QSpinBox(self))
			getattr(self,attrSPY).setRange(-150,150)
			getattr(self,attrSPY).setSingleStep(1)
			getattr(self,attrSPY).setValue(Y[i])

			grid.addWidget(getattr(self,attrSPX),i+2,0)
			grid.addWidget(getattr(self,attrSPY),i+2,1)

		LabelX= QtGui.QLabel("X (/100):")
		LabelY= QtGui.QLabel("Y (/100):")

		grid.addWidget(LabelX,1,0)
		grid.addWidget(LabelY,1,1)

		grid.addWidget(btnS)
		grid.addWidget(btnQ)

run()