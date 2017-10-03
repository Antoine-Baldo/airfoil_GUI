from airfoil_module import CST, create_x
import sys
import os 
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy
from PyQt4 import QtGui, QtCore

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	GUI.show()
	sys.exit(app.exec_())

def CSTMOD():

	chord = 1.
	x = create_x(chord, n = 20, distribution = 'polar')
	A0 = .2
	y = CST(x=x,c=1.,deltasz=[.2,.2],Au=[A0,.8,.2], Al = [.2,3,.4])
	pprint (x)
	pprint (y)

class Window(QtGui.QDialog):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)