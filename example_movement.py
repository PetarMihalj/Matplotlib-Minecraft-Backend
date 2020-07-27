from mc_mpl.mde import MDE
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
mpl.use("module://mc_mpl.mc_backend")

MDE().mc.player.setPos(0, 10, 0)

x = np.arange(-3, 3, 0.01)  # initialize the x axis range

plt.plot(x, x**2)
plt.gcf().move(50, 90)
plt.gcf().scale(1, 0.5)

fig, ax = plt.subplots(2, 1)
ax[0].plot(x, x)
ax[1].plot(x, np.sin(x))
plt.show()  # rendering is initialized via plt.show()

input()  # since this is a guy backend, you have to pause it, or it will auto-close
