import pandas as pd
df = pd.read_csv('elastic-const_all.csv')
c11 = df['C11']
c22 = df['C22']
c66 = df['C66']

s = 0
for i in range(len(c11)):
    if (c11[i]>0) and (c22[i]>0) and (c66[i]>0):
       print(i)
       s+=1

print(s)
