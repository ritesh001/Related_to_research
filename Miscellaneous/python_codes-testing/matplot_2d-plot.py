import numpy as np
import matplotlib.pyplot as plt

B = np.linspace(0,20,250)
c = ['red','green','blue','yellow','orange']

for n in range(5):
    l = 'n=%d' %n
    E_p = np.sqrt(2 * B * (n+1))
    E_m = -np.sqrt(2 * B * (n+1))
    plt.plot(B, E_p, color=c[n], label=l)
    plt.plot(B, E_m, color=c[n])

plt.legend(loc='upper left')
plt.title('Prob 3 : Landau energy levels(E) vs B for graphene')
plt.xlabel('Magnetic field (T) -->'); plt.ylabel('Energy (eV) --->')
# plt.xticks(np.arange(5,20,4))
plt.show()
