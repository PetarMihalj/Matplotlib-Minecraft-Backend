import matplotlib as mpl
import mpl_pi
mpl.use("module://mpl_pi")


rend = mpl_pi.RendererMC(5,5,5)

fig = mpl.figure.Figure()
ax=fig.add_axes((0,0,5,5))
ax.plot([1,2])
fig.draw(rend)
