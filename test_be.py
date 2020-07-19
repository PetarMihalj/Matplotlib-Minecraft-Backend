import matplotlib as mpl
import mpl_pi
mpl.use("module://mpl_pi")
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (1,1)
mpl.rcParams['lines.markersize'] = 1

import numpy as np
import time

plt.get_current_fig_manager().SetPosition((5, 0))

x=np.arange(-1,3,0.01)

plt.plot(x,np.exp(x))
plt.plot(x,x**2,'go')
plt.draw()


