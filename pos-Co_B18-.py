import math as m
#System = Co@B7
#1.0000000000
#  15.0000000000    0.0000000000    0.0000000000
#   0.0000000000   15.0000000000    0.0000000000
#   0.0000000000    0.0000000000   10.0000000000
#B Co
#7 1
#Cartesian
#   9.4820000000    7.5000000000    5.0000000000
#   8.7357567873    9.0495899983    5.0000000000
#   7.0589635089    9.4323071219    5.0000000000
#   5.7142797038    8.3599575709    5.0000000000
#   5.7142797038    6.6400424291    5.0000000000
#   7.0589635089    5.5676928781    5.0000000000
#   8.7357567873    5.9504100017    5.0000000000
#   7.5000000000    7.5000000000    5.0000000000
th = (2*m.pi)/7
r = 1.982
x0 = 7.5
y0 = 7.5
b=[]
c=[]
print("System = Co@B7")
print("{:12.10f}".format(1))
print("{:15.10f} {:15.10f} {:15.10f}".format(15,0,0))
print("{:15.10f} {:15.10f} {:15.10f}".format(0,15,0))
print("{:15.10f} {:15.10f} {:15.10f}".format(0,0,10))
print("B","Co")
print(18,1)
print("Cartesian")
for i in range(7):
    x = x0 + r*m.cos(i*th)
    b.append(x)
    y = y0 + r*m.sin(i*th)
    c.append(y)
    z = 5.0
    print("{:15.10f} {:15.10f} {:15.10f}".format(x,y,z))
th1 = (2*m.pi)/6
for i in range(6):
    x = r*m.cos(i*th1) + b[0]
    y = r*m.sin(i*th1) + c[0]
    z = 5.0
    print("{:15.10f} {:15.10f} {:15.10f}".format(x,y,z))
for i in range(6):
    x = r*m.cos(i*th1) + b[1]
    y = r*m.sin(i*th1) + c[1]
    z = 5.0
    print("{:15.10f} {:15.10f} {:15.10f}".format(x,y,z))
for i in range(6):
    x = r*m.cos(i*th1) + b[2]
    y = r*m.sin(i*th1) + c[2]
    z = 5.0
    print("{:15.10f} {:15.10f} {:15.10f}".format(x,y,z))
for i in range(6):
    x = r*m.cos(i*th1) + b[5]
    y = r*m.sin(i*th1) + c[5]
    z = 5.0
    print("{:15.10f} {:15.10f} {:15.10f}".format(x,y,z))
for i in range(6):
    x = r*m.cos(i*th1) + b[6]
    y = r*m.sin(i*th1) + c[6]
    z = 5.0
    print("{:15.10f} {:15.10f} {:15.10f}".format(x,y,z))
print("{:15.10f} {:15.10f} {:15.10f}".format(7.5,7.5,5.0))

