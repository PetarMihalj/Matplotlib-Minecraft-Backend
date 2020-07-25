import time

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams["figure.figsize"] = (0.3, 0.3)
mpl.rcParams["lines.markersize"] = 1
mpl.interactive(True)
mpl.use("module://mc_backend")

plt.ion()
print("INT:", mpl.is_interactive())
plt.plot([1, 2, 1])
plt.draw()

# plt.draw()
# plt.draw()


time.sleep(10)
