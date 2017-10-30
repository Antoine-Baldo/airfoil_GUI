from airfoil_module import CST
from CST_3D_module import *
import sys
import os
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import math
import numpy as np
from PyQt4 import QtGui, QtCore
from scipy.interpolate import interp1d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

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
		self.setWindowTitle('3D CST Module Controle')
		self.setWindowIcon(QtGui.QIcon('images.png'))
		grid = QtGui.QGridLayout()
		self.setLayout(grid)
		btnQ = QtGui.QPushButton('Quit', self)
		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)

		def run_3D_CST():
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			# Inputs
			# One of the diameters
			initial_chord = 1.
			# Nosecone height
			span = 4.
			# Shape coefficient for cross section (if A=1, circular, otherwise it is an ellipse)
			A = 1.
			# location of the nosecone tip
			nosecone_x = 0.2
			# Class coefficient for chord distribution (Nb=.5, elliptical, Nb=1, Haack series)
			Nb = 1.
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

			#B = [[1,1], [1.,1]]
			B = [[A], [A]]
			Na = 1.
			x = np.linspace(0,1)
		    
			[X,Y,Z_u, Z_l] = CST_3D(B, B, mesh =(50,50), span=span,
			                        N={'eta':[0,1], 'N1':[.5, .5], 'N2':[.5, .5]},
			                        chord = {'eta':[0,1], 'A':[1.], 'N1':Na, 'N2':Nb, 'initial_chord':initial_chord},
			                        sweep = {'eta':[0,1], 'A':[.5], 'N1':Nb, 'N2':Na, 'x_LE_final':nosecone_x})

			fig = plt.figure()
			ax = fig.gca(projection='3d')
			surf_u = ax.plot_surface(X, Z_u, Y, cmap=plt.get_cmap('jet'),
			                   linewidth=0, antialiased=False)
			surf_l = ax.plot_surface(X, Z_l, Y, cmap=plt.get_cmap('jet'),
			                   linewidth=0, antialiased=False)
			# cset = ax.contour(X, Z_u, Y, zdir='z', offset=0, cmap=cm.coolwarm)
			# cset = ax.contour(X, Z_l, Y, zdir='z', offset=0,  cmap=cm.coolwarm)
			# cset = ax.contour(X, Z_u, Y, zdir='x', offset=-.1, cmap=cm.coolwarm)
			# cset = ax.contour(X, Z_l, Y, zdir='x', offset=-.1, cmap=cm.coolwarm)
			# cset = ax.contour(X, Z_u, Y, zdir='y', offset =0.5,  cmap=cm.coolwarm)
			# cset = ax.contour(X, Z_l, Y, zdir='y', offset =0.5,  cmap=cm.coolwarm)

			# Customize the z axis.
			ax.set_zlim(0, 4)

			max_range = np.array([X.max()-X.min(),  Z_u.max()-Z_l.min(), Y.max()-Y.min()]).max() / 2.0

			mid_x = (X.max()+X.min()) * 0.5
			mid_y = (Y.max()+Y.min()) * 0.5
			mid_z = (Z_u.max()+Z_l.min()) * 0.5
			ax.set_xlim(mid_x - max_range, mid_x + max_range)
			ax.set_ylim(mid_z - max_range, mid_z + max_range)
			ax.set_zlim(mid_y - max_range, mid_y + max_range)
			plt.show()

