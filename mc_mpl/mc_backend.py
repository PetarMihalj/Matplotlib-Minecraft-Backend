from matplotlib.backend_bases import FigureCanvasBase
from matplotlib.backend_bases import FigureManagerBase, _Backend

import matplotlib as mpl

from mc_mpl.mde import MDE
from mc_mpl.mc_renderer import RendererMC


class FigureCanvasMC(FigureCanvasBase):
    def __init__(self, figure):
        print("init canvas")
        super().__init__(figure)

        # initialized in superclass constructor
        self.figure: mpl.figure.Figure
        self.manager: "FigureManagerMC"

        # self.callbacks.connect("close_event", self.my_close_event)
        # self.callbacks.connect("draw_event", self.my_close_event)

    # pylint: disable=unused-argument
    def draw(self, *vargs, **kvargs):
        """
        Draw the figure using the renderer.
        """
        print("drawing")
        # self.manager.window.points.clear()
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
        print("done")


class FigureManagerMC(FigureManagerBase):
    def __init__(self, canvas, num):
        super().__init__(canvas, num)
        size = canvas.figure.get_size_inches() * canvas.figure.dpi
        print(size)

        self.window = MDE().create_window(
            dims=(int(size[0]), 1, int(size[1])))
        print("here")
        # initialized in superclass constructor
        self.canvas: FigureCanvasMC

    def show(self):
        print("showing")
        # self.canvas.draw()
        self.window.render()

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

    @staticmethod
    def trigger_manager_draw(manager):
        manager.show()
