from mc_mpl.mde import MDE
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use("module://mc_mpl.mc_backend")

MDE().mc.player.setPos(0, 10, 0)

plt.plot([1, 2, 1])
plt.plot([1, 2, 1])
plt.show()

input()
