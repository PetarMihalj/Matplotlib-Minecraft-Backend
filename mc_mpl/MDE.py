from dataclasses import dataclass
import mcpi.minecraft


class Window:
    def __init__(self, pos, dims, _render_callback, _focus_callback):
        self.pos = pos
        self.dims = dims

        self.points = []
        self._render_callback = _render_callback
        self._focus_callback = _focus_callback

    def move(self, pos):
        self.pos = pos

    def resize(self, dims):
        self.dims = dims

    def add_point(self, point):
        self.points.append(point)

    def focus(self):
        self._focus_callback(self)

    def render(self):
        self._render_callback()


class MDE:
    def __init__(self):
        self.connect()
        self.next_focus_time = 0

        # maps windows to focus time
        self.focus_time = dict()

        self.last_rendered_points = []

    def connect(self):
        self.mc = mcpi.minecraft.Minecraft.create(
            address=mpl.rcParams.get("mc_mpl.ip", "127.0.0.1"),
            port=mpl.rcParams.get("mc_mpl.port", 4711),
        )

    def create_window(self, pos, dims):
        w = Window(pos, dims, self._render_callback, self._focus_callback)
        self.focus_time[w] = self.next_focus_time
        self.next_focus_time += 1
        return w

    def _render_callback(self):
        for (x, y, z, block_id, block_data) in self.last_rendered_points:
            self.mc.setBlock(y, z, x, mcpi.block.AIR)

        for w, prio in sorted(
            self.focus_time.items(), key=lambda x: x[1], reverse=True
        ):
            self.mc.setBlocks(
                *w.pos,
                w.pos[0] + w.dims[0] - 1,
                w.pos[1] + w.dims[1] - 1,
                w.pos[2] + w.dims[2] - 1,
                mcpi.block.AIR
            )
            for (x, y, z, block_id, block_data) in w.points:
                self.mc.setBlock(y, z, x, block_id, block_data)
                self.last_rendered_points.append((x, y, z))

    def _focus_callback(self, window):
        self.focus_time[w] = self.next_focus_time
        self.next_focus_time += 1

