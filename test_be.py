import matplotlib as mpl
import mpl_pi
mpl.use("module://mpl_pi")
import matplotlib.pyplot as plt

import numpy as np
import time

x=np.arange(-1,3,0.01)

plt.plot(x,x)
plt.draw()


