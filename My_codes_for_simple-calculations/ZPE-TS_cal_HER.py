import math as m
f=open("c","r")
for line in f:
    a=line.split()
Z = 0
S0 = 0
k = 8.627E-5
T = 298.15
d=[]
th=[]
for i in range(len(a)):
    a[i] = float(a[i])
    d.append(a[i]*2)
    th.append(d[i]/k)
    Z += a[i]
#print Z
for i in range(len(th)):
    if th[i] == 0:
       continue
    p = th[i]/T
    q = m.exp(p)
    r = m.log(1-(q**(-1)))
    S0+=r
S = k*S0
print Z - (0.20 - (T*S))
