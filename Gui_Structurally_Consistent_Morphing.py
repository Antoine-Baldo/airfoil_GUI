
"Programmed by Antoine BALDO"

from morphing import calculate_dependent_shape_coefficients
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
		self.setGeometry(200,50,1100,680)
		self.setWindowTitle('Structurally Consistent Control')
		self.setWindowIcon(QtGui.QIcon('images.png'))

		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		self.fig = Figure() 
		self.canvas = FigureCanvas(self.fig)
		grid.addWidget(self.canvas,0,0,2,-1)

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

			for i in range (5):
				attrSPACu.append('spAC_u' + str(i+1))
				attrSPpsispar.append('sppsi_spar' + str(i+1))

				V_AC_u.append(float((getattr(self,attrSPACu[i])).value())/100000)
				V_psi_spar.append(float((getattr(self,attrSPpsispar[i])).value())/100)

			print '##############################################################'
			print 'V_AC_u: ',V_AC_u
			print 'V_psi_spar: ',V_psi_spar

			AC_u1 = V_AC_u[0]
			AC_u2 = V_AC_u[1]
			AC_u3 = V_AC_u[2]
			AC_u4 = V_AC_u[3]
			AC_u5 = V_AC_u[4]

			psi_spar1 = V_psi_spar[0]
			psi_spar2 = V_psi_spar[1]
			psi_spar3 = V_psi_spar[2]
			psi_spar4 = V_psi_spar[3]
			psi_spar5 = V_psi_spar[4]
			psi_spars = [psi_spar1, psi_spar2, psi_spar3, psi_spar4, psi_spar5]

			Au_C, Al_C, c_C, spar_thicknesses = calculate_dependent_shape_coefficients(
                                                            V_AC_u,
                                                            psi_spars, Au_P, Al_P,
                                                            deltaz, c_P, morphing=morphing_direction)
			np.set_printoptions(precision=20)

			ax = self.fig.add_subplot(111)
			ax.clear()

			# Print shape for children
			x = np.linspace(0, c_C, 100000)
			y = CST(x, c_C, deltasz= [deltaz/2., deltaz/2.],  Al= Al_C, Au =Au_C)
			ax.plot(x, y['u'],'b',label = 'Children', lw=2)
			ax.plot(x, y['l'],'b',label = None, lw=2)

			# Print shape for parent
			x = np.linspace(0, c_P, 100000)
			y = CST(x, c_P, deltasz= [deltaz/2., deltaz/2.],  Al= Al_P, Au =Au_P)
			ax.plot(x, y['u'],'r--',label='Parent', lw=2)
			ax.plot(x, y['l'],'r--',label = None, lw=2)

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

			ax.set_xlabel('$\psi^p$', fontsize = 20)
			ax.set_ylabel(r'$\xi^p$', fontsize = 20)
			ax.set_ylim([-0.17,0.17])
			ax.grid()
			ax.set_aspect('equal', adjustable='box')
			ax.legend(loc=1)
			self.canvas.draw()

		btnS = QtGui.QPushButton('Start', self)
		btnS.clicked.connect(structurally_consistent)

		ValACu = [14870 ,10843,15084,10919,12840]
		Valpsispar = [20,30,50,70,90]

		for i in range (5):
			attrSPACu = 'spAC_u'+str(i+1)
			setattr(self, attrSPACu, QtGui.QSpinBox(self))
			getattr(self,attrSPACu).setRange(0,100000)
			getattr(self,attrSPACu).setSingleStep(100)
			getattr(self,attrSPACu).setValue(ValACu[i])

			attrSPpsispar = 'sppsi_spar'+str(i+1)
			setattr(self, attrSPpsispar, QtGui.QSpinBox(self))
			getattr(self,attrSPpsispar).setRange(0,100)
			getattr(self,attrSPpsispar).setSingleStep(100)
			getattr(self,attrSPpsispar).setValue(Valpsispar[i])

			grid.addWidget(getattr(self,attrSPACu),i+3,0)
			grid.addWidget(getattr(self,attrSPpsispar),i+3,1)

		LabelACu= QtGui.QLabel("ACu (/100000):")
		Labelpsispqar= QtGui.QLabel("psi spars (/10):")

		grid.addWidget(LabelACu,2,0)
		grid.addWidget(Labelpsispqar,2,1)
		grid.addWidget(btnS)
		grid.addWidget(btnQ)


run()