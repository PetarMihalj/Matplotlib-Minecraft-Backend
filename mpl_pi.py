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

    def __init__(self, width, height, dpi):
        RendererBase.__init__(self)
        print('here')
        self.dpi = dpi
        self.width = width
        self.height = height

    def draw_path(self, gc, path, transform, rgbFace=None):
        # docstring inherited
        lastpoint=[0,0]
        for point,code in path.iter_segments(curves=False):
            point=transform.transform(point)
            if code==1:
                lastpoint=point
            elif code==2 or code==79:
                utils.plotLine(int(lastpoint[0]),int(lastpoint[1]), int(point[0]), int(point[1]),
                    lambda i,j: RendererMC.mc.setBlock(i,70,-j,mcpi.block.WOOL.id,0)
                )
                lastpoint=point        

    def get_canvas_width_height(self):
        return self.width, self.height

    def clear(self):
        pass

    def option_image_nocomposite(self):
        # docstring inherited

        # It is generally faster to composite each image directly to
        # the Figure, and there's no file size benefit to compositing
        # with the Agg backend
        return True

    def option_scale_image(self):
        # docstring inherited
        return False


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
            self.renderer = RendererMC(w, h, self.figure.dpi)
            self._lastKey = key
        elif cleared:
            self.renderer.clear()
        return self.renderer

@_Backend.export
class MPLBackend(_Backend):
    print('here')
    FigureCanvas = FigureCanvasMC
    FigureManager = FigureManagerBase
