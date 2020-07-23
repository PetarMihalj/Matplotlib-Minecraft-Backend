from matplotlib.backend_bases import Gcf
from matplotlib.backend_bases import RendererBase, FigureCanvasBase
from matplotlib.backend_bases import FigureManagerBase, _Backend, GraphicsContextBase

import mcpi.minecraft as minecraft
import mcpi.block as block
import utils as utils

import matplotlib as mpl
import numpy as np


def rti(x):
    return int(round(x))


import MDE

mde = MDE.MDE()


class RendererMC(RendererBase):

    # closure which draws a point and fills drawn_point array
    def draw_point(self, i, j, k, block_id=block.WOOL.id, block_data=0):
        self.drawn_points.append((i, j, k))

    def clear(self):
        for i, j, k in self.drawn_points:
            mc.setBlock(j, k, i, block.AIR)
        self.drawn_points.clear()

    def __init__(self, l, b, w, h, dpi, bbox):
        RendererBase.__init__(self)
        self.drawn_points = []
        self.height = 10
        self.l = l
        self.b = b
        self.w = w
        self.h = h
        self.dpi = dpi
        self.bbox = bbox

    def get_canvas_width_height(self):
        return self.w, self.h

    def draw_path(self, gc, path, transform, rgbFace=None):
        lastpoint = [0, 0]

        for point, code in path.iter_segments(
            curves=False,
            transform=transform,
            # clip=transform.transform_bbox(self.bbox).bounds,
        ):
            point = point + [self.l, self.b]

            if code == 1:
                lastpoint = point
                firstpoint = point
            elif code == 2:
                utils.plotLine(
                    rti(lastpoint[0]),
                    rti(lastpoint[1]),
                    rti(point[0]),
                    rti(point[1]),
                    lambda i, j: self.draw_point(
                        i, j, self.height, block_data=utils.rgb_to_wool_data(rgbFace)
                    ),
                )
                lastpoint = point
            elif code == 79:
                utils.plotLine(
                    rti(lastpoint[0]),
                    rti(lastpoint[1]),
                    rti(firstpoint[0]),
                    rti(firstpoint[1]),
                    lambda i, j: self.draw_point(
                        i, j, self.height, block_data=utils.rgb_to_wool_data(rgbFace)
                    ),
                )
                firstpoint = point
                lastpoint = point


class FigureCanvasMC(FigureCanvasBase):
    def my_close_event(self, event):
        print("caught")

    def __init__(self, figure):
        super().__init__(figure)
        self.callbacks.connect("close_event", self.my_close_event)
        self.callbacks.connect("draw_event", self.my_close_event)

    def draw(self):
        """
        Draw the figure using the renderer.
        """
        self.renderer = self.get_renderer(cleared=True)
        self.figure.draw(self.renderer)

    def get_renderer(self, cleared=False):
        l, b, w, h = self.figure.bbox.bounds
        # key = w, h, self.figure.dpi

        if not hasattr(self, "renderer"):
            self.renderer = RendererMC(l, b, w, h, self.figure.dpi, self.figure.bbox)
        if cleared:
            self.renderer.clear()
        return self.renderer


class FigureManagerMC(FigureManagerBase):
    def __init__(self, canvas, num):
        super().__init__(canvas, num)

    def destroy(self):
        self.canvas.renderer.clear()


@_Backend.export
class MPLBackend(_Backend):
    FigureCanvas = FigureCanvasMC
    FigureManager = FigureManagerMC
