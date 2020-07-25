from matplotlib.backend_bases import RendererBase

import mc_mpl.mcpi.block as block


def rti(x):
    return int(round(x))


def plot_line_low(x0, y0, x1, y1, f):
    """
    Adapted for python from https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    """
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    d = 2 * dy - dx
    y = y0

    for x in range(x0, x1 + 1):
        f(x, y)
        if d > 0:
            y = y + yi
            d = d - 2 * dx
        d = d + 2 * dy


def plot_line_high(x0, y0, x1, y1, f):
    """
    Adapted for python from https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    """
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    d = 2 * dx - dy
    x = x0

    for y in range(y0, y1 + 1):
        f(x, y)
        if d > 0:
            x = x + xi
            d = d - 2 * dy
        d = d + 2 * dx


def plot_line(x0, y0, x1, y1, f):
    """
    Adapted for python from https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    """
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            # pylint: disable=arguments-out-of-order
            plot_line_low(x1, y1, x0, y0, f)
        else:
            plot_line_low(x0, y0, x1, y1, f)
    else:
        if y0 > y1:
            # pylint: disable=arguments-out-of-order
            plot_line_high(x1, y1, x0, y0, f)
        else:
            plot_line_high(x0, y0, x1, y1, f)


def rgb_to_wool_data(rgbface):
    if rgbface is None:
        r, g, b = (0, 0, 0)
    else:
        r, g, b, _ = rgbface
    r *= 256
    g *= 256
    b *= 256

    data = [
        (233, 236, 236, 0),
        (240, 118, 19, 1),
        (189, 68, 179, 2),
        (58, 175, 217, 3),
        (248, 198, 39, 4),
        (112, 185, 25, 5),
        (237, 141, 172, 6),
        (62, 68, 71, 7),
        (142, 142, 134, 8),
        (21, 137, 145, 9),
        (121, 42, 172, 10),
        (53, 57, 157, 11),
        (114, 71, 40, 12),
        (84, 109, 27, 13),
        (161, 39, 34, 14),
        (20, 21, 25, 15),
    ]
    closest = min(data, key=lambda x: abs(
        x[0] - r) + abs(x[1] - g) + abs(x[2] - b))
    return closest[3]


class RendererMC(RendererBase):
    def __init__(self, l, b, w, h, dpi, bbox, draw_point_callback):
        RendererBase.__init__(self)
        self.l = l
        self.b = b
        self.w = w
        self.h = h
        self.dpi = dpi
        self.bbox = bbox
        self.dpc = draw_point_callback

    def draw_image(self, gc, x, y, im, transform=None):
        raise NotImplementedError()

    def draw_path(self, gc, path, transform, rgbFace=None):
        def drawing_closure(x, y):
            return self.dpc(
                (x, 0, y, block.WOOL.id, rgb_to_wool_data(rgbFace))
            )
        lastpoint = [0, 0]

        for point, code in path.iter_segments(curves=False, transform=transform,):
            point = point + [self.l, self.b]
            if code == 1:
                lastpoint = point
                firstpoint = point
            elif code == 2:
                plot_line(
                    rti(lastpoint[0]),
                    rti(lastpoint[1]),
                    rti(point[0]),
                    rti(point[1]),
                    drawing_closure,
                )
                lastpoint = point
            elif code == 79:
                plot_line(
                    rti(lastpoint[0]),
                    rti(lastpoint[1]),
                    rti(firstpoint[0]),
                    rti(firstpoint[1]),
                    drawing_closure,
                )
                firstpoint = point
                lastpoint = point
