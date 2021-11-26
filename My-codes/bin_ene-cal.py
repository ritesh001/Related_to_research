f=open("ads_ener","r")
b=[]
for line in f:
    a=line.split()
    a=float(a[0])
    b.append(a)

for i in range(0,len(b),4):
    c=b[i+2]+b[i+3]
    d=b[i+1]-c
    print("{:5.1f} {:15.10f}".format(b[i],d))
