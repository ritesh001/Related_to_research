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
for i in range(2,38):                                                    # for C2N
#for i in range(38,62):                                                    # for C3N3
     c = 4-float(b[i][4])                                                 # 4 valence electrons on C
#     print("Charge on C{} = {:8.4f}".format(int(b[i][0]), c))
     sum_C += c

#Printing charge on N
for i in range(62,80):                                                   # for C2N
#for i in range(80,104):                                                   # for C3N3
     d = float(b[i][4])-5                                                 # 5 valence electrons on N
     e = -d
#     print("Charge on N{} = {:8.4f}".format(int(b[i][0])-60, e))
     sum_N += e   

#print("Total_charge =", sum_C + sum_N)


#Min charge on N and max charge on C

C_charges=[]
N_charges=[]
for i in range(2,62):
    g = 4-float(b[i][4])
    C_charges.append(g)

C_max = max(C_charges)
print("Max charge on C =", C_max, "with carbon no =", C_charges.index(C_max)+1)

for i in range(62,104):
    h = 5 - float(b[i][4])
    N_charges.append(h)

N_min = min(N_charges)
print("Min charge on N =", N_min, "with nitrogen no =", N_charges.index(N_min)+1)

