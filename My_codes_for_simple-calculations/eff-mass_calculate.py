import math as m
A = float(input("Enter coeffient of x^2:"))         #from fitted parabola in xmgrace (through regression)
a = float(input("Enter lattice parameter (in angstroms):"))
a *= 10**(-10)                                      #converting to meter
grad_E = 2*A                                        #d2E/dk2 
grad_E *= 1.6*10**(-19)                             #converting eV to J
h_bar = 1.054588664*10**(-34)
c = 2*m.pi/a                                        #Conversion factor for k
eff_mass = (h_bar*h_bar*c*c)/grad_E
eff_mass /= 9.1*10**(-31)                           #Dividing by mass of electron (in kg)
print("effective mass =", eff_mass)
