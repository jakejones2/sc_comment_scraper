import os
import pathlib

def check_merged_dir(dir):
    dir = pathlib.PurePath(dir)
    dir = dir.with_suffix('.csv')
    count = 1
    if not os.path.exists(dir.as_posix()):
        return dir.as_posix()
    dir = dir.with_stem(dir.stem + f'({count})')
    while True:
        if not os.path.exists(dir.as_posix()):
            return dir.as_posix()
        new = count + 1
        dir.stem = dir.stem.replace(f'({count})', f'({new})')
        count += 1



    # dir = dir[:-4] + f'({count}).csv'
    # while True:
    #     if not os.path.exists(dir):
    #         return dir
    #     new = count + 1
    #     dir = dir.replace(f'({count})', f'({new})')
    #     count += 1


        
def check_ind_dir(dir, filters):
    if not filters.filtername:
        dir = dir.split('[')[0]
    dir = dir[:-3] + '].csv'
    count = 1
    if not os.path.exists(dir):
        return dir
    dir = dir[:-4] + f'({count}).csv'    
    while True:
        if not os.path.exists(dir):
            return dir
        new = count + 1
        dir = dir.replace(f'({count})', f'({new})')
        count += 1

            
        
#use a generator?
