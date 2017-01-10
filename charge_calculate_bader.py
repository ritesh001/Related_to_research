import math as m
f=open("ACF.dat","r")
b=[]

sum_C = 0
sum_N = 0

#Reading file
for line in f:
    a = line.split()
    a = [a[i] for i in range(len(a))]
    b.append(a)
#print(b)

#Printing charge on C
for i in range(38,62):
     c = 4-float(b[i][4])
     print("Charge on C{} = {:8.4f}".format(int(b[i][0]), c))
     sum_C += c

#Printing charge on N
for i in range(80,104):
     d = float(b[i][4])-5
     e = -d
     print("Charge on N{} = {:8.4f}".format(int(b[i][0]), e))
     sum_N += e   

print("Total_charge =", sum_C + sum_N)
