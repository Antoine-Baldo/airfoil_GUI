"Programed by Antoine BALDO"

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

		# Intialization of the windows' parametres:
		self.setGeometry(125,35,1100,725)
		self.setWindowTitle('3D CST Module Controle')
		self.setWindowIcon(QtGui.QIcon("C:/Users/antoi/OneDrive/Documents/GitHub/airfoil_GUI/images.png"))

		# Creation of the Layout:
		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		# Intialization of the Figure:
		self.fig = plt.figure()
		self.canvas = FigureCanvas(self.fig)

		#Pedro's program
		def run_3D_CST():
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			# Inputs
			# One of the diameters 
			initial_chord = float(self.le_initial_chord.text())
			# Nosecone height
			span = float(self.le_span.text())
			# Shape coefficient for cross section (if A=1, circular, otherwise it is an ellipse)
			A = float(self.le_A.text())
			# location of the nosecone tip
			nosecone_x = float(self.le_nosecone_x.text())
			# Class coefficient for chord distribution (Nb=.5, elliptical, Nb=1, Haack series)
			Nb = float(self.le_Nb.text())
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			B = [[A], [A]]
			Na = 1.
			x = np.linspace(0,1)
		    
			[X,Y,Z_u, Z_l] = CST_3D(B, B, mesh =(50,50), span=span,
			                        N={'eta':[0,1], 'N1':[.5, .5], 'N2':[.5, .5]},
			                        chord = {'eta':[0,1], 'A':[1.], 'N1':Na, 'N2':Nb, 'initial_chord':initial_chord},
			                        sweep = {'eta':[0,1], 'A':[.5], 'N1':Nb, 'N2':Na, 'x_LE_final':nosecone_x})

			ax = self.fig.gca(projection='3d')
			ax.clear()
			surf_u = ax.plot_surface(X, Z_u, Y, cmap=plt.get_cmap('jet'),
			                   linewidth=0, antialiased=False)
			surf_l = ax.plot_surface(X, Z_l, Y, cmap=plt.get_cmap('jet'),
			                   linewidth=0, antialiased=False)

			# Customize the z axis.
			ax.set_zlim(0, 4)

			max_range = np.array([X.max()-X.min(),  Z_u.max()-Z_l.min(), Y.max()-Y.min()]).max() / 2.0

			mid_x = (X.max()+X.min()) * 0.5
			mid_y = (Y.max()+Y.min()) * 0.5
			mid_z = (Z_u.max()+Z_l.min()) * 0.5
			ax.set_xlim(mid_x - max_range, mid_x + max_range)
			ax.set_ylim(mid_z - max_range, mid_z + max_range)
			ax.set_zlim(mid_y - max_range, mid_y + max_range)
			self.canvas.draw()

		# Export program
		def export_STL():


			print '\n'"Data exported"'\n'

		# Creation of the 5 Lines Edits
		# Creation of the initial chord Lines Edits:
		Label1 = QtGui.QLabel("Initial chord, one of the diameters (between 0.1 and 1):")
		self.le_initial_chord = QtGui.QLineEdit(self)
		self.le_initial_chord.setText("1")

		# Creation of the Nosecone height Lines Edits:
		Label2 = QtGui.QLabel("Nosecone height (between 0.1 and 10):")
		self.le_span = QtGui.QLineEdit(self)
		self.le_span.setText("4")

		# Creation of the Shape coefficient for cross section Lines Edits:
		Label3 = QtGui.QLabel("Shape coefficient for cross section, for 1 it is circular, otherwise it is an ellipse (between 0.1 and 10):")
		self.le_A = QtGui.QLineEdit(self)
		self.le_A.setText("1")

		# Creation of the location of the nosecone tip Lines Edits:
		Label4 = QtGui.QLabel("Nosecone tip location (between -5 and 5):")
		self.le_nosecone_x = QtGui.QLineEdit(self)
		self.le_nosecone_x.setText("0.2")

		# Creation of the Class coefficient for chord distribution Lines Edits:
		Label5 = QtGui.QLabel("Chord distribution, for 0.5 it is elliptical, and for 1 it is Haack series (between 0.5 and 1):")
		self.le_Nb = QtGui.QLineEdit(self)
		self.le_Nb.setText("1")

		# Creation of the 'Run' button:
		btnR = QtGui.QPushButton('Run', self)
		btnR.clicked.connect(run_3D_CST)

		# Creation of the 'Quit' button:
		btnQ = QtGui.QPushButton('Quit', self)
		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)

		# Creation of the 'Export' button:
		btnE = QtGui.QPushButton('Export', self)
		btnE.clicked.connect(export_STL)

		# Pedro's formule picture:
		LabelP = QtGui.QLabel()
		pixmap = QtGui.QPixmap("C:/Users/antoi/OneDrive/Documents/GitHub/airfoil_GUI/images.png")
		LabelP.setPixmap(pixmap)

		# Add the differents windows elements 
		grid.addWidget(self.canvas,0,0,1,-1)
		grid.addWidget(LabelP,1,0,-1,1)
		grid.addWidget(Label1,1,1)
		grid.addWidget(self.le_initial_chord,1,2)
		grid.addWidget(Label2,2,1)
		grid.addWidget(self.le_span,2,2)
		grid.addWidget(Label3,3,1)
		grid.addWidget(self.le_A,3,2)
		grid.addWidget(Label4,4,1)
		grid.addWidget(self.le_nosecone_x,4,2)
		grid.addWidget(Label5,5,1)
		grid.addWidget(self.le_Nb,5,2)
		grid.addWidget(btnR,6,1,1,-1)
		grid.addWidget(btnE,7,1)
		grid.addWidget(btnQ,7,2)

run()