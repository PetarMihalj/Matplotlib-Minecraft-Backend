from io import StringIO
import sys
import mc_backend
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use("module://mc_backend")

plt.rcParams["figure.figsize"] = (1, 1)
mpl.rcParams['lines.markersize'] = 1


plt.draw()


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


while True:
    time.sleep(1)
    for msg in mc_backend.mc.player.pollChatPosts():
        if len(msg.message) > 0 and msg.message[0] == '%':
            try:
                out = eval(msg.message[1:])
                mc_backend.mc.postToChat(out)
            except BaseException as error:
                mc_backend.mc.postToChat(error)
        else:
            try:
                with Capturing() as out:
                    exec(msg.message)
                mc_backend.mc.postToChat(out)
            except BaseException as error:
                mc_backend.mc.postToChat(error)
