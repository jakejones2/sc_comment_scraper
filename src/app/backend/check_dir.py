import os
import pathlib


def check_merged_dir(dir):
    dir = pathlib.PurePath(dir).with_suffix(".csv")
    count = 1
    if not os.path.exists(dir.as_posix()):
        return dir.as_posix()
    dir = dir.with_stem(dir.stem + f"({count})")
    while True:
        if not os.path.exists(dir.as_posix()):
            return dir.as_posix()
        new = count + 1
        dir = dir.with_stem(dir.stem.replace(f"({count})", f"({new})"))
        count += 1


def check_ind_dir(dir, filters):
    if filters.filtername:
        dir += f"[filters = {filters.filtername[:-2]}]"
    dir = pathlib.PurePath(dir).with_suffix(".csv")
    count = 1
    if not os.path.exists(dir.as_posix()):
        return dir.as_posix()
    dir = dir.with_stem(dir.stem + f"({count})")
    while True:
        if not os.path.exists(dir.as_posix()):
            return dir.as_posix()
        new = count + 1
        dir = dir.with_stem(dir.stem.replace(f"({count})", f"({new})"))
        count += 1
