import itertools

import mc_mpl.mcpi.minecraft as minecraft
import mc_mpl.singleton as singleton
import mc_mpl.mcpi.block as block


class Window:
    def __init__(
        self,
        pos,
        dims,
        _render_callback,
        _focus_callback,
        _destroy_callback,
        _clear_screen_callback,
    ):
        self.pos = pos
        self.dims = dims

        # this is a part of public interface
        # lazy until render() called
        self.points = []
        self.signs = []
        self.right_click_callbacks = []

        self._render_callback = _render_callback
        self._focus_callback = _focus_callback
        self._destroy_callback = _destroy_callback
        self._clear_screen_callback = _clear_screen_callback

    def move(self, pos):
        self._clear_screen_callback()
        self.pos = pos
        self._render_callback()

    def resize(self, dims):
        self._clear_screen_callback()
        self.dims = dims
        self._render_callback()

    def focus(self):
        self._clear_screen_callback()
        self._focus_callback(self)
        self._render_callback()

    def close(self):
        self._clear_screen_callback()
        self.points.clear()
        self.signs.clear()
        self._destroy_callback(self)
        self._render_callback()

    def render(self):
        self._render_callback()


class MDE(metaclass=singleton.Singleton):
    def __init__(self, address="127.0.0.1", port=4711):
        self.mc = minecraft.Minecraft.create(address=address, port=port)
        self.next_focus_time = 0

        # maps windows to focus time
        self.focus_time = dict()
        self.last_rendered_points = []

    def create_window(self, pos=(0, 10, 0), dims=(50, 2, 50)):
        w = Window(
            pos,
            dims,
            self._render_callback,
            self._focus_callback,
            self._destroy_callback,
            self._clear_screen_callback,
        )
        self.focus_time[w] = self.next_focus_time
        self.next_focus_time += 1
        return w

    def _render_callback(self):
        for w, _ in sorted(self.focus_time.items(), key=lambda x: x[1]):
            self._draw_cube_relative_to_window(
                w,
                0,
                0,
                0,
                w.dims[0] - 1,
                w.dims[1] - 1,
                w.dims[2] - 1,
                block.AIR.id,
                0,
            )
            for point in w.points:
                self._draw_point_relative_to_window(w, *point)

            for sign in w.signs:
                self._draw_sign_relative_to_window(w, *sign)

            for p1, p2 in get_cuboid_sides(*w.dims):
                self._draw_cube_relative_to_window(
                    w, *p1, *p2, block.GOLD_BLOCK.id, 0
                )

    def _clear_screen_callback(self):
        rendered_points_backup = list(self.last_rendered_points)
        self.last_rendered_points.clear()
        for (w, x, y, z, _, _) in rendered_points_backup:
            self._draw_point_relative_to_window(
                w, x, y, z, block.AIR.id, 0)

    def _focus_callback(self, window):
        self.focus_time[window] = self.next_focus_time
        self.next_focus_time += 1

    def _destroy_callback(self, window):
        del self.focus_time[window]

    def _draw_point_relative_to_window(self, w, x, y, z, block_id, block_data):
        if (
            #x >= 0
            # and x < w.dims[0] - 0
            y >= 0
            and y < w.dims[1] - 0
            and z >= 0
            and z < w.dims[2] - 0
        ):
            self.mc.setBlock(
                -x + w.pos[0], y + w.pos[1], z +
                w.pos[2], block_id, block_data,
            )
            self.last_rendered_points.append(
                (w, x, y, z, block_id, block_data,))

    def _draw_sign_relative_to_window(self, w, x, y, z, line):
        if (
            #x >= 0
            # and x < w.dims[0] - 0
            y >= 0
            and y < w.dims[1] - 0
            and z >= 0
            and z < w.dims[2] - 0
        ):
            self.mc.setSign(
                -x + w.pos[0], y + w.pos[1], z +
                w.pos[2], 63, 8, line
            )
            # this doesnt mattter for deletion, act as if block was placed
            self.last_rendered_points.append(
                (w, x, y, z, 63, 8,))

    def _draw_cube_relative_to_window(
        self, w, x1, y1, z1, x2, y2, z2, block_id, block_data
    ):
        x1 = max(x1, 0)
        x2 = min(x2, w.dims[0] - 1)
        y1 = max(y1, 0)
        y2 = min(y2, w.dims[1] - 1)
        z1 = max(z1, 0)
        z2 = min(z2, w.dims[2] - 1)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    # print("cubing", file=sys.stderr)
                    self.mc.setBlock(
                        -x + w.pos[0],
                        y + w.pos[1],
                        z + w.pos[2],
                        block_id,
                        block_data,
                    )
                    self.last_rendered_points.append(
                        (w, x, y, z, block_id, block_data,)
                    )


def get_cuboid_sides(x, y, z):
    vertices = itertools.product([0, x - 1], [0, y - 1], [0, z - 1])
    sides = [
        (x, y)
        for x, y in itertools.product(vertices, repeat=2)
        if int(x[0] != y[0]) + int(x[1] != y[1]) + int(x[2] != y[2]) == 1
    ]
    return sides


if __name__ == "__main__":
    import matplotlib as mpl

    mpl.rcParams["figure.figsize"] = (0.3, 0.3)
    mpl.rcParams["lines.markersize"] = 1

    mpl.use("module://mc_backend")
    import matplotlib.pyplot as plt

    plt.ion()
    MDE().mainloop()
