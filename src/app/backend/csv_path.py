'''A couple of functions dealing with filenames and paths for 
CSV files'''

import os
import pathlib
from app.backend.paths import MyPaths
from tkinter import messagebox


def create_ind_dir(url, filters, scrape_datetime, num):

    '''When csv files are created individually, this function attempts
    to extract the artist and track names from the url to form the
    basis of the file name. Any filters used are appended to the name
    in square brackets. Duplicates are named with parentheses'''

    try:
        # extracting names from url
        track = url.split("/")[-1]
        artist = url.split("/")[-2]
        if "?" in track:
            track = track.split("?")[0]
        # stored in folder based on time of scraping (should ensure no duplicates)
        dir = f"{MyPaths.csv_path}/{scrape_datetime:%Y-%m-%d %H.%M}/{artist}, {track}"
    except:
        # if url structure or song/artist name is unusual
        messagebox.showwarning(
            "Filename Error",
            f"Failed to extract track name from {url}, file numbered instead.",
        )
        dir = (
            f"csv_exports/{scrape_datetime:%Y-%m-%d %H.%M}/url_{num}"
        )
    # add filtername and suffix
    if filters.filtername:
        dir += f"[filters = {filters.filtername[:-2]}]"
    dir = pathlib.PurePath(dir).with_suffix(".csv")
    # check for duplicates and rename in form file(1) etc.
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


def create_merged_dir(settings):

    '''This function ensures that the custom filename has a suffix of .csv
    and that any duplicate files are renamed as file(1), file(2) etc.'''

    dir = f"{MyPaths.csv_path}/{settings.csvfilename}"
    dir = pathlib.PurePath(dir).with_suffix(".csv")
    count = 1
    if not os.path.exists(dir.as_posix()):
        return dir.as_posix()
    # if the path already exists, rename the file as file(1)
    dir = dir.with_stem(dir.stem + f"({count})")
    while True:
        if not os.path.exists(dir.as_posix()):
            return dir.as_posix()
        # if this still fails, try file(x + 1)
        new = count + 1
        dir = dir.with_stem(dir.stem.replace(f"({count})", f"({new})"))
        count += 1
