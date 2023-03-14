import os

def check_merged_dir(dir):
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
