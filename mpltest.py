
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

x=np.arange(-1,1,0.01)
plt.plot(x,x*x)
plt.savefig('a.png')