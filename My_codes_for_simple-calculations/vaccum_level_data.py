f = open("test", "r")
b=[]
for line in f:
    a = line.split()
    a = [float(a[i]) for i in range(len(a))]
    b.append(a)
#print(b)
c=[0 for j in range(len(b))]
#for i in range(len(b)):
#    c.append(b[i][3])
#d=min(c)
#e=c.index(d)
f=0
x=0
for i in range(len(b)):
    c[i] = b[i][0]*b[i][1]
    x += b[i][0]
    f += c[i]
print f/x
    
