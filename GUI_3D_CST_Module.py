from airfoil_module import CST
from 3D_CST_module import *
import sys
import os
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import math
import numpy as np
from PyQt4 import QtGui, QtCore
from scipy.interpolate import interp1d

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	GUI.show()
	sys.exit(app.exec_())

# class Window(QtGui.QDialog):
# 	def __init__(self, parent=None):
# 		super(Window, self).__init__(parent)
# 		_fromUtf8 = QtCore.QString.fromUtf8
# 		self.setGeometry(200,50,1100,650)
# 		self.setWindowTitle('3D CST Module Controle')
# 		self.setWindowIcon(QtGui.QIcon('images.png'))
# 		btnQ = QtGui.QPushButton('Quit', self)
# 		btnQ.clicked.connect(QtCore.QCoreApplication.instance().quit)

def CST_3D():

	psi = np.linspace(0,1,mesh[0])
    eta = np.linspace(0,1,mesh[1])

    zeta_u = np.zeros(mesh)
    zeta_l = np.zeros(mesh)
    for i in range(mesh[0]):
        for j in range(mesh[1]):
            zeta_u[j][i] = C(N, psi[i], eta[j])*S(Bu, psi[i], eta[j])
            zeta_l[j][i] = -C(N, psi[i], eta[j])*S(Bl, psi[i], eta[j])
    print eta
    print chord['initial_chord']
    print chord['A']
    print chord['N1'], chord['N2']
    chord_distribution = CST(eta, chord['eta'][1], chord['initial_chord'], Au=chord['A'], N1=chord['N1'], N2=chord['N2'])
    sweep_distribution = CST(eta, sweep['eta'][1], deltasz = sweep['x_LE_final']-.5*chord['initial_chord'], Au=sweep['A'], N1=sweep['N1'], N2=sweep['N2'])
    chord_distribution = chord_distribution[::-1]
    sweep_distribution = sweep_distribution
    # taper_function(eta, shape = 'linear', N)
    x = np.zeros(len(psi))
    for i in range(len(x)):
        x[i] = psi[i]*chord_distribution[i]
    print chord_distribution
    print sweep_distribution
    print x
    print psi
    y = eta

    X = np.zeros(mesh)
    Y = np.zeros(mesh)
    Z_u = np.zeros(mesh)
    Z_l = np.zeros(mesh)
    for i in range(mesh[0]):
        for j in range(mesh[1]):
            X[j][i] = psi[i]*chord_distribution[j] - sweep_distribution[j] -.5*chord['initial_chord']
        
            Y[j][i] = span*eta[j]
            Z_u[j][i] = zeta_u[j][i]*chord_distribution[j]
            Z_l[j][i] = zeta_l[j][i]*chord_distribution[j]
    return [X,Y,Z_u,Z_l]

if __name__ == '__main__':
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from matplotlib import cm

    
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

 CST_3D()
