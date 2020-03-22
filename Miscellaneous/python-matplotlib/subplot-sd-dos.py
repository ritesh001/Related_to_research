import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#d = ['dxy.dat','dyz.dat','dxz.dat','dz2.dat','dx2.dat']
metals = ['Ag','Co','Cr','Cu','Fe','Mn','Mo','Nb','Ni','Pd','Rh','Ru','V']
#files = []; m = sys.argv[1]
#for i in range(len(d)):
#	name = m + '-' + d[i]
#	files.append(name)

counter = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2), (3,0),
           (3,1), (3,2), (4,0), (4,1), (4,2)]

fig, axs = plt.subplots(5,3, sharex=True, figsize=(8,8), constrained_layout=True)

s = 0
min_x = -1.0; max_x = 2.0

## taken from internet ;-)
def autoscale_y(axs,margin=0.1):
    """This function rescales the y-axis based on the data that is visible given the current xlim of the axis.
    ax -- a matplotlib axes object
    margin -- the fraction of the total height of the y-data to pad the upper and lower ylims"""

    def get_bottom_top(line):
        xd = line.get_xdata()
        yd = line.get_ydata()
        lo,hi = axs.get_xlim()
        y_displayed = yd[((xd>lo) & (xd<hi))]
        h = np.max(y_displayed) - np.min(y_displayed)
        bot = np.min(y_displayed)-margin*h
        top = np.max(y_displayed)+margin*h
        return bot,top

    lines = axs.get_lines()
    bot,top = np.inf, -np.inf

    for line in lines:
        new_bot, new_top = get_bottom_top(line)
        if new_bot < bot: bot = new_bot
        if new_top > top: top = new_top

    axs.set_ylim(bot,top)
##

curr_dir = os.getcwd()
for m in metals:
    os.chdir('./%s' %(m))
    file = '%s-her.dat' %(m)
    f = pd.read_table(file, sep="\s+")   ## for reading .dat file in block format ---> very important
    col = f.columns
    # for i in range(5):
    x = f[col[0]]
    x2 = [0 for j in range(len(x))]
    y1 = f[col[3]]
    y2 = f[col[4]]
    y3 = f[col[5]]
    y4 = f[col[6]]
    y5 = f[col[7]]
    y6 = f[col[8]]
#    tit = fil.strip('.dat')
    # print(f)
#    axs[counter[s]].plot(x, y1, color='black')
#    axs[counter[s]].plot(x, y2, color='black')
#    axs[counter[s]].plot(x, y3, color='gray', label='%s s' %(m))
    axs[counter[s]].plot(x, y3, color='gray')
    axs[counter[s]].plot(x, y4, color='gray')
    axs[counter[s]].plot(x, y5, color='cyan')
    axs[counter[s]].plot(x, y6, color='cyan')
#    axs[counter[s]].plot(x2, y1, marker='_', color='red')
    axs[counter[s]].set_xlim([min_x, max_x])
    # axs[counter[s]].autoscale(enable=True, axis='y', tight=True)
    autoscale_y(axs[counter[s]])
    axs[counter[s]].set_title(m, fontsize=10)
    axs[counter[s]].fill_between(x, 0, y3, color='gray')
    axs[counter[s]].fill_between(x, y4, 0, color='gray')
#    axs[counter[s]].legend()
    # print(counter[s])
    s += 1
    os.chdir(curr_dir)

# print(y1.shape())
# plt.plot(x,y1)
plt.show()
#plt.savefig('./%s-d-orbitals_subplot.png' %(m))
