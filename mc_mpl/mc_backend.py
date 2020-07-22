from matplotlib.backend_bases import Gcf
from matplotlib.backend_bases import RendererBase, FigureCanvasBase
from matplotlib.backend_bases import FigureManagerBase,_Backend,GraphicsContextBase

import mcpi.minecraft as minecraft
import mcpi.block as block
import utils as utils

import numpy as np
import threading
import matplotlib as mpl

def rti(x):
    return int(round(x))

mc = minecraft.Minecraft.create(
    address=mpl.rcParams.get('mc_mpl.ip', '127.0.0.1'),
    port=mpl.rcParams.get('mc_mpl.port', 4711)
)

class RendererMC(RendererBase):
    """
    The renderer handles all the drawing primitives using a graphics
    context instance that controls the colors/styles
    """
    lock = threading.RLock()

    def __init__(self, l,b,w,h, dpi,bbox):
        RendererBase.__init__(self)
        self.height=10

        self.l=l
        self.b=b
        self.w=w
        self.h=h
        self.dpi=dpi
        self.bbox=bbox

    def get_canvas_width_height(self):
        return self.w, self.h

    def draw_path(self, gc, path, transform, rgbFace=None):
        # docstring inherited
        lastpoint=[0,0]
        #gc
        #print(gc.get_clip_rectangle())
        
        for point,code in path.iter_segments(curves=False,transform=transform,
          clip=transform.transform_bbox(self.bbox).bounds):
            point=point+[self.l,self.b]

            if code==1:
                lastpoint=point
                firstpoint=point
            elif code==2:
                utils.plotLine(rti(lastpoint[0]),rti(lastpoint[1]), rti(point[0]), rti(point[1]),
                    lambda i,j: mc.setBlock(j,self.height,i
                        ,block.WOOL.id,utils.rgb_to_wool_data(rgbFace))
                )
                lastpoint=point        
            elif code==79:
                utils.plotLine(rti(lastpoint[0]),rti(lastpoint[1]), rti(firstpoint[0]), rti(firstpoint[1]),
                    lambda i,j: mc.setBlock(j,self.height,i
                        ,block.WOOL.id,utils.rgb_to_wool_data(rgbFace))
                )
                firstpoint=point
                lastpoint=point        

    def clear(self):
        print('clearing')
        for i in range(rti(self.l),rti(self.l+self.w)+1):
            for j in range(rti(self.b),rti(self.b+self.h)+1):
                mc.setBlock(j,self.height,i,block.AIR)
                
    #def new_gc(self):
        # docstring inherited
       # return None #GraphicsContextTemplate()



class FigureCanvasMC(FigureCanvasBase):
    def draw(self):
        """
        Draw the figure using the renderer.
        """
        self.renderer = self.get_renderer(cleared=True)

        self.figure.draw(self.renderer)

        # A GUI class may be need to update a window using this draw, so
        # don't forget to call the superclass.
        super().draw()

    def draw_idle(self):
        self.draw()

    def get_renderer(self, cleared=False):
        l, b, w, h = self.figure.bbox.bounds
        #key = w, h, self.figure.dpi

        if not hasattr(self, "renderer"):
            self.renderer = RendererMC(l,b,w,h,self.figure.dpi,self.figure.bbox)
        if cleared:
            self.renderer.clear()
        return self.renderer

@_Backend.export
class MPLBackend(_Backend):
    FigureCanvas = FigureCanvasMC
    FigureManager = FigureManagerBase
