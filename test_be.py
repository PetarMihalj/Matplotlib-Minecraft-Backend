import matplotlib as mpl
import mpl_pi
mpl.use("module://mpl_pi")
import matplotlib.pyplot as plt
import numpy as np

rend = mpl_pi.RendererMC()

fig = mpl.figure.Figure((1,1))
ax=fig.add_axes((0,0,1,1))

x=np.arange(-1,1,0.01)
ax.plot(x,x*x,'r:')

fig.draw(rend)
fig.clear()
