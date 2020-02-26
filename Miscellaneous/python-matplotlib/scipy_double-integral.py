import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import dblquad

a = 2.46
gamma = -2.7
b = (np.sqrt(3)*a)/2.0; c = a / 2.0

#omega = np.linspace(-3,3,20)

w = np.linspace(-3.2,3.2,20)
rho = np.zeros(20)
for i in range(len(w)):
    def integrand(x,y):
        mod_fk_sq = 1 + (4 * np.cos(b * x) * np.cos(c * y)) + (4 * (np.cos(c * y))**2)
        E1 = gamma * np.sqrt(mod_fk_sq)
        E2 = -E1
        c1 = (w[i] - E1 + 0.02j)**(-1); c2 = (w[i] - E2 + 0.02j)**(-1)
        A = -2 * (c1.imag + c2.imag)
        return A

    ans, err = dblquad(integrand, -np.pi/2.46, np.pi/2.46,
                       lambda x : -np.pi/2.46,
                       lambda x : np.pi/2.46)

    rho[i] = ans

plt.plot(w,rho)
plt.show()
