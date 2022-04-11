f = open("energy.dat", "r")
b=[]
for line in f:
    a = line.split()
    a = [float(a[i]) for i in range(len(a))]
    b.append(a)
#print(b)
c=[]
for i in range(len(b)):
    c.append(b[i][3])
d=min(c)
e=c.index(d)
#for i in range(len(b)):
#    e=b[i][3].index(d)
print b[e][4], b[e][5]
