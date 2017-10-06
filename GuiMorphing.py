
"Programmed by Antoine BALDO"

from morphing.py import calculate_dependent_shape_coefficients, calculate_shape_coefficients_tracing
from airfoil_module import CST
from CST_module import *
import sys
import os 
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import numpy
from PyQt4 import QtGui, QtCore

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	GUI.show()
	sys.exit(app.exec_())