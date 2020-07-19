from matplotlib.backend_bases import Gcf
from matplotlib.backend_bases import RendererBase,FigureCanvasBase,FigureManagerBase,_Backend

import mcpi.minecraft
import mcpi.block

import numpy as np
import utils

class RendererMC(RendererBase):
    """
    The renderer handles all the drawing primitives using a graphics
    context instance that controls the colors/styles
    """
    mc = mcpi.minecraft.Minecraft.create()

    def __init__(self):
        RendererBase.__init__(self)

    def draw_path(self, gc, path, transform, rgbFace=None):
        # docstring inherited
        lastpoint=[0,0]
        for point,code in path.iter_segments(curves=False):
            point=transform.transform(point)
            if code==1:
                lastpoint=point
            elif code==2 or code==79:
                utils.plotLine(int(lastpoint[0]),int(lastpoint[1]), int(point[0]), int(point[1]),
                    lambda i,j: RendererMC.mc.setBlock(i,45,-j
                        ,mcpi.block.WOOL.id,utils.rgb_to_wool_data(rgbFace))
                )
                
                lastpoint=point        

    def clear(self):
        print("clearing")


class FigureCanvasMC(FigureCanvasBase):
    def draw(self):
        """
        Draw the figure using the renderer.
        """
        print('here')
        self.renderer = self.get_renderer(cleared=True)
        self.figure.draw(self.renderer)
        # A GUI class may be need to update a window using this draw, so
        # don't forget to call the superclass.
        super().draw()

    def get_renderer(self, cleared=False):
        print('here')
        l, b, w, h = self.figure.bbox.bounds
        key = w, h, self.figure.dpi
        reuse_renderer = (hasattr(self, "renderer")
                          and getattr(self, "_lastKey", None) == key)
        if not reuse_renderer:
            self.renderer = RendererMC()
            self._lastKey = key
        elif cleared:
            self.renderer.clear()
        return self.renderer

@_Backend.export
class MPLBackend(_Backend):
    print('here')
    FigureCanvas = FigureCanvasMC
    FigureManager = FigureManagerBase
