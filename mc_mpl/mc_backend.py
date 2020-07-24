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
    def __init__(self, l, b, w, h, dpi, bbox, draw_point_callback):
        RendererBase.__init__(self)
        self.drawn_points = []
        self.height = 10
        self.l = l
        self.b = b
        self.w = w
        self.h = h
        self.dpi = dpi
        self.bbox = bbox
        self.dpc = draw_point_callback

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
            drawing_closure = lambda x, y: self.dpc(
                (x, y, 10, block.WOOL.id, utils.rgb_to_wool_data(rgbFace))
            )

            if code == 1:
                lastpoint = point
                firstpoint = point
            elif code == 2:
                utils.plotLine(
                    rti(lastpoint[0]),
                    rti(lastpoint[1]),
                    rti(point[0]),
                    rti(point[1]),
                    drawing_closure,
                )
                lastpoint = point
            elif code == 79:
                utils.plotLine(
                    rti(lastpoint[0]),
                    rti(lastpoint[1]),
                    rti(firstpoint[0]),
                    rti(firstpoint[1]),
                    drawing_closure,
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
        l, b, w, h = self.figure.bbox.bounds
        self.renderer = RendererMC(
            l,
            b,
            w,
            h,
            self.figure.dpi,
            self.figure.bbox,
            self.manager.window.add_point,
        )

        self.figure.draw(self.renderer)
        self.manager.window.render()

    def draw_idle(self):
        self.draw()


class FigureManagerMC(FigureManagerBase):
    def __init__(self, canvas, num):
        self.window = mde.create_window()
        super().__init__(canvas, num)

    def show(self):
        self.window.focus()
        self.window.render()

    def destroy(self):
        self.window.destroy()
        self.window.render()

    def resize(self, w, h):
        self.window.resize((w, h, 1))

    def move(self, x, y):
        self.window.move((x, y, 10))


@_Backend.export
class MPLBackend(_Backend):
    FigureCanvas = FigureCanvasMC
    FigureManager = FigureManagerMC
