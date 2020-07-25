import contextlib
import time
import io
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from mc_mpl.mde import MDE

mpl.rcParams["figure.figsize"] = (1, 1)
mpl.rcParams["lines.markersize"] = 1
mpl.use("module://mc_mpl.mc_backend")


@contextlib.contextmanager
def capturing_stdout():
    backup = sys.stdout
    sys.stdout = io.StringIO()
    yield sys.stdout
    sys.stdout = backup


MDE().mc.player.setPos(0, 10, 0)
while True:
    time.sleep(1)
    for msg in MDE().mc.player.pollChatPosts():
        if len(msg.message) > 0 and msg.message[0] == "%":
            try:
                # pylint: disable=eval-used
                out = eval(msg.message[1:])
                MDE().mc.postToChat(out)
            # pylint: disable=broad-except
            except BaseException as error:
                MDE().mc.postToChat(error)
        else:
            try:
                out: io.StringIO
                with capturing_stdout() as out:
                    # pylint: disable=exec-used
                    exec(msg.message)
                MDE().mc.postToChat(out)
            # pylint: disable=broad-except
            except BaseException as error:
                MDE().mc.postToChat(error)
        plt.show()
