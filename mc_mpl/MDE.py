from dataclasses import dataclass
import mcpi.minecraft


class Window:
    def __init__(self, pos, dims, _render_callback, _focus_callback, _destroy_callback):
        self._pos = pos
        self._dims = dims

        #this is a part of public interface
        #lazy until render() called
        self.points = []

        self._render_callback = _render_callback
        self._focus_callback = _focus_callback
        self._destroy_callback = _destroy_callback

    def move(self, pos):
        self._pos = pos
        self._render_callback()

    def resize(self, dims):
        self._dims = dims
        self._render_callback()

    def focus(self):
        self._focus_callback(self)
        self._render_callback()

    def close(self):
        self.clear()
        self._destroy_callback(self)
        self._render_callback()

    def render(self):
        self._render_callback()

        
import singleton
class MDE(metaclass = singleton.Singleton):
    def __init__(self, ADDRESS="127.0.0.1" PORT=4711):
        self._connect(ADDRESS, PORT)
        self.next_focus_time = 0

        # maps windows to focus time
        self.focus_time = dict()

        self.last_rendered_points = []

    def _connect(self, ADDRESS, PORT):
        self.mc = mcpi.minecraft.Minecraft.create(address=ADDRESS, port=PORT)

    def create_window(self, pos=(0, 0, 0), dims=(50, 50, 1)):
        w = Window(
            pos,
            dims,
            self._render_callback,
            self._focus_callback,
            self._destroy_callback,
        )
        self.focus_time[w] = self.next_focus_time
        self.next_focus_time += 1
        return w

    def _render_callback(self):
        print("render callback MDE")
        for (x, y, z, block_id, block_data) in self.last_rendered_points:
            self.mc.setBlock(y, z, x, mcpi.block.AIR)
        self.last_rendered_points.clear()

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
                self.mc.setBlock(
                    y + w.pos[0], z + w.pos[1], x + w.pos[2], block_id, block_data
                )
                self.last_rendered_points.append(
                    (x + w.pos[0], y + w.pos[1], z + w.pos[2], block_id, block_data)
                )

    def _focus_callback(self, window):
        self.focus_time[window] = self.next_focus_time
        self.next_focus_time += 1

    def _destroy_callback(self, window):
        del self.focus_time[window]


instance = MDE()
