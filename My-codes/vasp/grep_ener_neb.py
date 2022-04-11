f=open("energies","r")
b=[]
for line in f:
    a=line.split()
    a=float(a[0])
    b.append(a)
c=b[0]
b.sort()
print(b[5]-c)
