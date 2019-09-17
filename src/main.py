#!/usr/bin/env python
import glob
import os

from util import apply_theme, run

if __name__ == "__main__":
    for theme in glob.glob("themes/*.dunstrc"):
        fname = os.path.basename(theme).split(".")[0]
        run(theme, "/tmp/showcase/{}.png".format(fname))
