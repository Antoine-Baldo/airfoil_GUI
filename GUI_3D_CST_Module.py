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
		self.setGeometry(200,50,1100,650)
		self.setWindowTitle('3D CST Module Controle')
		self.setWindowIcon(QtGui.QIcon('images.png'))

		# Creation of the Layout:
		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		# Intialization of the Figure:
		self.fig = plt.figure()
		self.canvas = FigureCanvas(self.fig)

		#Pedro's program
		def run_3D_CST():
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			# initial_chord range = [0.1,1.]
			# span range = [0.1,10]
			# A range= [0.1,10]
			# nosecone_x range = [-5,5]
			# Nb range = [0.5,1]
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			# Inputs
			# One of the diameters
			initial_chord = int(self.sl_initial_chord.value())/10
			# Nosecone height
			span = int(self.sl_span.value())/10
			# Shape coefficient for cross section (if A=1, circular, otherwise it is an ellipse)
			A = int(self.sl_A.value())/10
			# location of the nosecone tip
			nosecone_x = int(self.sl_nosecone_x.value())/10
			# Class coefficient for chord distribution (Nb=.5, elliptical, Nb=1, Haack series)
			Nb = int(self.sl_Nb.value())/10
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

			#B = [[1,1], [1.,1]]
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
			self.canvas.draw()

		# Creation of the 5 sliders:
		# Creation of the initial chord slider:
		Label1 = QtGui.QLabel("Initial chord (/10):")
		self.sl_initial_chord = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.sl_initial_chord.setMinimum(1)
		self.sl_initial_chord.setMaximum(10)
		self.sl_initial_chord.setValue(10)

		# Creation of the Nosecone height slider:
		Label2 = QtGui.QLabel("Nosecone height (/10):")
		self.sl_span = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.sl_span.setMinimum(1)
		self.sl_span.setMaximum(100)
		self.sl_span.setValue(40)

		# Creation of the Shape coefficient for cross section slider:
		Label3 = QtGui.QLabel("Shape coefficient for cross section (/10):")
		self.sl_A = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.sl_A.setMinimum(1)
		self.sl_A.setMaximum(100)
		self.sl_A.setValue(10)

		# Creation of the the nosecone tip slider:
		Label4 = QtGui.QLabel("Cosecone tip (/10):")
		self.sl_nosecone_x = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.sl_nosecone_x.setMinimum(-50)
		self.sl_nosecone_x.setMaximum(50)
		self.sl_nosecone_x.setValue(2)

		# Creation of the the chord distribution slider:
		Label5 = QtGui.QLabel("Chord distribution (/10):")
		self.sl_Nb = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.sl_Nb.setMinimum(5)
		self.sl_Nb.setMaximum(10)
		self.sl_Nb.setValue(10)

		# Creation of the 5 spinbox:
		# Creation of the initial chord spinbox:
		self.sp_initial_chord = QtGui.QSpinBox(self)
		self.sp_initial_chord.setRange(1, 10)
		self.sp_initial_chord.setSingleStep(1)
		self.sp_initial_chord.setValue(10)

		# Creation of the Nosecone height spinbox:
		self.sp_span = QtGui.QSpinBox(self)
		self.sp_span.setRange(1, 100)
		self.sp_span.setSingleStep(1)
		self.sp_span.setValue(40)

		# Creation of the coefficient for cross section spinbox:
		self.sp_A = QtGui.QSpinBox(self)
		self.sp_A.setRange(1, 100)
		self.sp_A.setSingleStep(1)
		self.sp_A.setValue(10)

		# Creation of the location of the nosecone spinbox:
		self.sp_nosecone_x = QtGui.QSpinBox(self)
		self.sp_nosecone_x.setRange(-50, 50)
		self.sp_nosecone_x.setSingleStep(1)
		self.sp_nosecone_x.setValue(2)

		# Creation of the Class coefficient for chord distribution spinbox:
		self.sp_Nb = QtGui.QSpinBox(self)
		self.sp_Nb.setRange(5, 10)
		self.sp_Nb.setSingleStep(1)
		self.sp_Nb.setValue(10)

		#Connect the differents values from the sliders and the spinbox to eatch other:
		self.sl_initial_chord.valueChanged.connect(self.sp_initial_chord.setValue)
		self.sp_initial_chord.valueChanged.connect(self.sl_initial_chord.setValue)

		self.sl_span.valueChanged.connect(self.sp_span.setValue)
		self.sp_span.valueChanged.connect(self.sl_span.setValue)

		self.sl_A.valueChanged.connect(self.sp_A.setValue)
		self.sp_A.valueChanged.connect(self.sl_A.setValue)

		self.sl_nosecone_x.valueChanged.connect(self.sp_nosecone_x.setValue)
		self.sp_nosecone_x.valueChanged.connect(self.sl_nosecone_x.setValue)

		self.sl_Nb.valueChanged.connect(self.sp_Nb.setValue)
		self.sp_Nb.valueChanged.connect(self.sl_Nb.setValue)


		# Creation of the 'Run' button:
		btnR = QtGui.QPushButton('Run', self)
		btnR.clicked.connect(run_3D_CST)

		# Add the differents windows elements 
		grid.addWidget(self.canvas,0,0,1,-1)
		grid.addWidget(Label1,1,0)
		grid.addWidget(self.sp_initial_chord,2,0)
		grid.addWidget(self.sl_initial_chord,2,1)
		grid.addWidget(Label2,3,0)
		grid.addWidget(self.sp_span,4,0)
		grid.addWidget(self.sl_span,4,1)
		grid.addWidget(Label3,5,0)
		grid.addWidget(self.sp_A,6,0)
		grid.addWidget(self.sl_A,6,1)
		grid.addWidget(Label4,7,0)
		grid.addWidget(self.sp_nosecone_x,8,0)
		grid.addWidget(self.sl_nosecone_x,8,1)
		grid.addWidget(Label5,9,0)
		grid.addWidget(self.sp_Nb,10,0)
		grid.addWidget(self.sl_Nb,10,1)
		grid.addWidget(btnR,11,0,1,-1)

run()

