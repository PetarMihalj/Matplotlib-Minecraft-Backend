from matplotlib.backend_bases import Gcf
from matplotlib.backend_bases import RendererBase,FigureCanvasBase
from matplotlib.backend_bases import FigureManagerBase,_Backend,GraphicsContextBase

import mcpi.minecraft
import mcpi.block

import numpy as np
import utils
import threading

def rti(x):
    return int(round(x))

class RendererMC(RendererBase):
    """
    The renderer handles all the drawing primitives using a graphics
    context instance that controls the colors/styles
    """
    lock = threading.RLock()

    mc = mcpi.minecraft.Minecraft.create()

    def __init__(self, l,b,w, h, dpi,bbox):
        RendererBase.__init__(self)
        self.scaling=0.25
        self.height=225

        self.l=450
        self.b=-150
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
            point=point*self.scaling+[self.l,self.b]
            point*=[1,-1]
            point+=[0,self.b]

            if code==1:
                lastpoint=point
                firstpoint=point
            elif code==2:
                utils.plotLine(rti(lastpoint[0]),rti(lastpoint[1]), rti(point[0]), rti(point[1]),
                    lambda i,j: RendererMC.mc.setBlock(i,self.height,j
                        ,mcpi.block.WOOL.id,utils.rgb_to_wool_data(rgbFace))
                )
                lastpoint=point        
            elif code==79:
                utils.plotLine(rti(lastpoint[0]),rti(lastpoint[1]), rti(firstpoint[0]), rti(firstpoint[1]),
                    lambda i,j: RendererMC.mc.setBlock(i,self.height,j
                        ,mcpi.block.WOOL.id,utils.rgb_to_wool_data(rgbFace))
                )
                firstpoint=point
                lastpoint=point        

    def clear(self):
        print('clearing')
        for i in range(rti(self.l),rti(self.l+self.w*self.scaling)+1):
            for j in range(rti(self.b),rti(self.b+self.h*self.scaling)):
                RendererMC.mc.setBlock(i,self.height,j,mcpi.block.AIR)
                
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
        key = w, h, self.figure.dpi
        reuse_renderer = (hasattr(self, "renderer")
                          and getattr(self, "_lastKey", None) == key)

        if not reuse_renderer:
            self.renderer = RendererMC(l,b,w,h,self.figure.dpi,self.figure.bbox)
            self._lastKey = key
        elif cleared:
            self.renderer.clear()
        return self.renderer

@_Backend.export
class MPLBackend(_Backend):
    FigureCanvas = FigureCanvasMC
    FigureManager = FigureManagerBase
