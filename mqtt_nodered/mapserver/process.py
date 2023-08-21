#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from subprocess import call
import os, glob, random
from tqdm import tqdm

files = glob.glob("*.000")

# cmds = [
    # "DEPARE | grep DRVAL1",
    # "SOUNDG | grep EXPSOU",
    # "DEPCNT | grep VALDCO"]

# outs = []
# for f in files[:10]:
    # r = f"\n\n>> {f}\n"
    # for cmd in cmds:
        # c = f"ogrinfo {f} {cmd}"
        # out = call(c, shell=True)
        # r += f"> {c}\n{out}\n"
    # print(r)
    # outs.append(r)


# some_files = [random.choice(files) for i in range(20)]

output = "output/DEPCNT/LINESTRING"
os.makedirs(os.path.join(os.getcwd(), output), exist_ok=True)
for f in tqdm(files):
    call(f'ogr2ogr -skipfailure -append -f "ESRI Shapefile" {output} {f} -nlt LINESTRING DEPCNT', shell=True)
