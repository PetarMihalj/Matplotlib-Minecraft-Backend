from matplotlib.backend_bases import FigureCanvasBase
from matplotlib.backend_bases import FigureManagerBase, _Backend

import matplotlib as mpl
import matplotlib.pyplot as plt

from mc_mpl.mde import MDE
from mc_mpl.mc_renderer import RendererMC
import sys

mpl.rcParams["figure.figsize"] = (1, 1)
mpl.rcParams["lines.markersize"] = 1


class FigureCanvasMC(FigureCanvasBase):
    def __init__(self, figure):
        super().__init__(figure)

        # initialized in superclass constructor
        self.figure: mpl.figure.Figure
        self.manager: "FigureManagerMC"

        # injections for ease of use
        self.figure.move = lambda x, y: self.manager.move(x, y)
        self.figure.scale = lambda w, h: self.figure.set_size_inches(w, h)

    # pylint: disable=unused-argument
    def draw(self, *vargs, **kvargs):
        """
        Draw the figure using the renderer.
        """
        l, b, w, h = self.figure.bbox.bounds
        renderer = RendererMC(
            l,
            b,
            w,
            h,
            self.figure.dpi,
            self.figure.bbox,
            self.manager.window.points.append,
        )
        self.figure.draw(renderer)


class FigureManagerMC(FigureManagerBase):
    def __init__(self, canvas, num):
        super().__init__(canvas, num)
        size = canvas.figure.get_size_inches() * canvas.figure.dpi

        self.window = MDE().create_window(
            dims=(int(size[0]), 1, int(size[1])))

        # initialized in superclass constructor
        self.canvas: FigureCanvasMC

    def show(self):
        self.window.points.clear()
        self.canvas.draw()
        self.window.render()

    def destroy(self):
        self.window.close()

    def resize(self, w, h):
        self.window.resize((int(w),
                            1, int(h)))

    def move(self, x, y):
        self.window.move((x, 10, y))


@_Backend.export
class MPLBackend(_Backend):
    FigureCanvas = FigureCanvasMC
    FigureManager = FigureManagerMC

    @staticmethod
    def trigger_manager_draw(manager):
        manager.show()
