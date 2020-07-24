import mcpi.minecraft
import time
import numpy as np


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
        self._pos = pos
        self._dims = dims

        # this is a part of public interface
        # lazy until render() called
        self.points = []
        self.right_click_callbacks = []

        self._render_callback = _render_callback
        self._focus_callback = _focus_callback
        self._destroy_callback = _destroy_callback
        self._clear_screen_callback = _clear_screen_callback

    def move(self, pos):
        self._clear_screen_callback()
        self._pos = pos
        self._render_callback()

    def resize(self, dims):
        self._clear_screen_callback()
        self._dims = dims
        self._render_callback()
        print("resize finished")

    def focus(self):
        self._clear_screen_callback()
        self._focus_callback(self)
        self._render_callback()
        print("focus finished")

    def close(self):
        self._clear_screen_callback()
        self.points.clear()
        self._destroy_callback(self)
        self._render_callback()

    def render(self):
        self._render_callback()


import singleton
from utils import Capturing
import sys


class MDE(metaclass=singleton.Singleton):
    def __init__(self, ADDRESS="127.0.0.1", PORT=4711):
        self._connect(ADDRESS, PORT)
        self.next_focus_time = 0

        # maps windows to focus time
        self.focus_time = dict()
        self.last_rendered_points = []

    def mainloop(self):
        self.mc.player.setPos(0, 10, 0)
        while True:
            time.sleep(1)
            for msg in self.mc.player.pollChatPosts():
                if len(msg.message) > 0 and msg.message[0] == "%":
                    try:
                        out = eval(msg.message[1:])
                        self.mc.postToChat(out)
                    except BaseException as error:
                        self.mc.postToChat(error)
                        # print(error)
                else:
                    try:
                        with Capturing() as out:
                            exec(msg.message)
                            self.mc.postToChat(out)
                    except BaseException as error:
                        self.mc.postToChat(error)
                        # print(error)

    def _connect(self, ADDRESS, PORT):
        self.mc = mcpi.minecraft.Minecraft.create(address=ADDRESS, port=PORT)

    def create_window(self, pos=(0, 10, 0), dims=(50, 1, 50)):
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
        for w, prio in sorted(self.focus_time.items(), key=lambda x: x[1]):
            self._draw_cube_relative_to_window(
                w,
                0,
                0,
                0,
                w._dims[0] - 1,
                w._dims[1] - 1,
                w._dims[2] - 1,
                mcpi.block.AIR.id,
                0,
            )
            import utils

            for point in w.points:
                self._draw_point_relative_to_window(w, *point)

            for p1, p2 in utils.get_cuboid_sides(*w._dims):
                self._draw_cube_relative_to_window(
                    w, *p1, *p2, mcpi.block.GOLD_BLOCK.id, 0
                )

    def _clear_screen_callback(self):
        rendered_points_backup = list(self.last_rendered_points)
        self.last_rendered_points.clear()
        for (w, x, y, z, block_id, block_data) in rendered_points_backup:
            self._draw_point_relative_to_window(w, x, y, z, mcpi.block.AIR.id, 0)

    def _focus_callback(self, window):
        self.focus_time[window] = self.next_focus_time
        self.next_focus_time += 1

    def _destroy_callback(self, window):
        del self.focus_time[window]

    def _draw_point_relative_to_window(self, w, x, y, z, block_id, block_data):
        if (
            x >= 0
            and x < w._dims[0] - 0
            and y >= 0
            and y < w._dims[1] - 0
            and z >= 0
            and z < w._dims[2] - 0
        ):
            self.mc.setBlock(
                -x + w._pos[0], y + w._pos[1], z + w._pos[2], block_id, block_data,
            )
            self.last_rendered_points.append((w, x, y, z, block_id, block_data,))

    def _draw_cube_relative_to_window(
        self, w, x1, y1, z1, x2, y2, z2, block_id, block_data
    ):
        x1 = max(x1, 0)
        x2 = min(x2, w._dims[0] - 1)
        y1 = max(y1, 0)
        y2 = min(y2, w._dims[1] - 1)
        z1 = max(z1, 0)
        z2 = min(z2, w._dims[2] - 1)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    # print("cubing", file=sys.stderr)
                    self.mc.setBlock(
                        -x + w._pos[0],
                        y + w._pos[1],
                        z + w._pos[2],
                        block_id,
                        block_data,
                    )
                    self.last_rendered_points.append(
                        (w, x, y, z, block_id, block_data,)
                    )


import matplotlib as mpl

mpl.rcParams["figure.figsize"] = (0.3, 0.3)
mpl.rcParams["lines.markersize"] = 1

mpl.use("module://mc_backend")
import matplotlib.pyplot as plt

MDE().mainloop()

