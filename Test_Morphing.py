
"Programmed by Antoine BALDO"

from morphing import calculate_shape_coefficients_tracing
from morphing import calculate_dependent_shape_coefficients
from airfoil_module import CST
from CST_module import *
import sys
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt

morphing_direction = 'forwards'
inverted = False

ValX = [1,0.1 ,0.3,0.5,0.7]
ValY = [0,0.02,0.03,0.04,0.05]

Au_P =  [0.10887, 0.1187, 0.07843, 0.12084, 0.07919, 0.09840]
Al_P =  [0.11117, 0.1000, 0.1239, 0.06334, 0.11539, 0.10400]

Valpsispar = [0.2,0.3,0.5,0.7,0.9]
###################################################################################################################
###################################################################################################################
tip_displacement = {'x':ValX[0], 'y':ValY[0]}
chord =tip_displacement['x']

deltaz = tip_displacement['y']

other_points = {'x': [ValX[1],ValX[2],ValX[3],ValX[4]],'y': [ValY[1],ValY[2],ValY[3],ValY[4]]}

print Au_P[0], tip_displacement, other_points,chord, deltaz
A = calculate_shape_coefficients_tracing(Au_P[0], tip_displacement, other_points, 0.5, 1.,chord, deltaz)
print 'A:'
print A
# BREAK
y = np.linspace(0, tip_displacement['y'], 100000)
x = CST(y, tip_displacement['y'], deltasz= tip_displacement['x'],  Au = A, N1=0.5, N2=1.)
print tip_displacement

###################################################################################################################
###################################################################################################################

n = len(Au_P) - 1

attrSPACu = []
attrSPpsispar = []
V_AC_u = []
V_psi_spar = []

AC_u1 = Au_P[0]
AC_u2 = A[1]
AC_u3 = A[2]
AC_u4 = A[3]
AC_u5 = A[4]

psi_spars = Valpsispar

Au_C, Al_C, c_C, spar_thicknesses = calculate_dependent_shape_coefficients(
                                                    AC_u1, AC_u2, AC_u3, AC_u4, AC_u5,
                                                    psi_spars, Au_P, Al_P,
                                                    deltaz, chord, morphing=morphing_direction)
np.set_printoptions(precision=20)

# Print shape for children
x = np.linspace(0, c_C, 100000)
y = CST(x, c_C, deltasz= [deltaz/2., deltaz/2.],  Al= Al_C, Au =Au_C)
plt.plot(x, y['u'],'b',label = 'Children', lw=2)
plt.plot(x, y['l'],'b',label = None, lw=2)

# Print shape for parent
x = np.linspace(0, chord, 100000)
y = CST(x, c_P, deltasz= [deltaz/2., deltaz/2.],  Al= Al_P, Au =Au_P)
plt.plot(x, y['u'],'r--',label='Parent', lw=2)
plt.plot(x, y['l'],'r--',label = None, lw=2)

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
		plt.plot([x_children_j, x_children_j - spar_thicknesses[j]*s[0]],[y_children_j, y_children_j - spar_thicknesses[j]*s[1]], c = 'b', lw=2, label=None)
		psi_flats.append(x_children_j - spar_thicknesses[j]*s[0])
		y = CST(np.array([psi_parent_j*c_P]), c_P, deltasz=[deltaz/2., deltaz/2.], Al= Al_P, Au =Au_P)

		intersections_x_children.append(x_children_j - spar_thicknesses[j]*s[0])
		intersections_y_children.append(y_children_j - spar_thicknesses[j]*s[1])

		# Print spars for parents
		plt.plot([psi_parent_j*c_P, psi_parent_j*c_P], [y['u'], y['u']-spar_thicknesses[j]], 'r--', lw=2, label = None)

		intersections_x_parent.append(psi_parent_j*c_P)
		intersections_y_parent.append(y['u']-spar_thicknesses[j])

###################################################################################################################
###################################################################################################################