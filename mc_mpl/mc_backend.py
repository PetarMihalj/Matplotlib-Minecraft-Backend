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


class RendererMC(RendererBase):
    def __init__(self, l, b, w, h, dpi, bbox, draw_point_callback):
        print("new rend")
        RendererBase.__init__(self)
        self.drawn_points = []
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

        for point, code in path.iter_segments(curves=False, transform=transform,):

            point = point + [self.l, self.b]
            drawing_closure = lambda x, y: self.dpc(
                (x, 0, y, block.WOOL.id, utils.rgb_to_wool_data(rgbFace))
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
    def __init__(self, figure):
        print("init canvas")
        super().__init__(figure)

        # initialized in superclass constructor
        figure: mpl.Figure
        manager: "FigureManagerMC"

        # self.callbacks.connect("close_event", self.my_close_event)
        # self.callbacks.connect("draw_event", self.my_close_event)

    def draw(self):
        """
        Draw the figure using the renderer.
        """
        print("drawing")
        self.manager.window.points.clear()
        l, b, w, h = self.figure.bbox.bounds
        self.renderer = RendererMC(
            l,
            b,
            w,
            h,
            self.figure.dpi,
            self.figure.bbox,
            self.manager.window.points.append,
        )

        self.figure.draw(self.renderer)
        self.manager.window.render()
        print("done")


class FigureManagerMC(FigureManagerBase):
    def __init__(self, canvas, num):
        super().__init__(canvas, num)
        size = canvas.figure.get_size_inches() * canvas.figure.dpi
        print(size)
        import MDE

        self.window = MDE.MDE().create_window(dims=(int(size[0]), 1, int(size[1])))

        # initialized in superclass constructor
        self.canvas: FigureCanvasMC

        self.figure.close = self.destroy
        self.figure.resize = self.resize
        self.figure.move = self.move

    def show(self):
        print("showing")
        self.window.focus()

    def destroy(self):
        print("destroying")
        self.window.close()

    def resize(self, w, h):
        print("resizing")
        self.window.resize((int(w), 1, int(h)))

    def move(self, x, y):
        self.window.move((x, 10, y))


@_Backend.export
class MPLBackend(_Backend):
    FigureCanvas = FigureCanvasMC
    FigureManager = FigureManagerMC
