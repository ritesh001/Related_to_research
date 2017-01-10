TM = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn']
TM_energy = [-12.64765700/2,-23.32339200/3,-17.89210100/2,-18.98921700/2,-523.14489000/58,-16.61556100/2,-14.17961900/2,-22.25644300/4,-14.85590400/2,-2.56855320/2]
a = float(input("Enter energy of system (AB) :"))
b = float(input("Enter energy of pristine (A) :"))
c = int(input("Enter code for TM (0-9) :"))
form_energy = a - b - TM_energy[c]
print form_energy
