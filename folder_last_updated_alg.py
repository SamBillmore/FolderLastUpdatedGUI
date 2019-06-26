from pathlib import Path
from datetime import datetime
import pandas as pd
import more_itertools

def latest_update_to_sub_dirs(directory, progress, progress_bar):
    """
    Loops through each first level sub directory in a specified directory and returns a pandas dataframe a row for each 
    sub directory containing:
    - the sub directory name
    - the date the folder was last modified
    Returns the output as a pandas dataframe
    Also updates progress, a tkinter ProgressBar
    """
    list_folders_dates = []
    progress.set(0)
    progress_bar.update_idletasks()
    max_count = more_itertools.ilen(Path(directory).iterdir())
    for path in Path(directory).iterdir():
        progress.set(progress.get() + (100/max_count))
        progress_bar.update_idletasks()
        if path.is_dir():
            time = path.stat().st_mtime
            list_folders_dates.append([path.name, datetime.fromtimestamp(time)])

    return pd.DataFrame(list_folders_dates,columns=['Folder','Date last modified']).sort_values(by=['Date last modified'])

def latest_file_in_direct_sub_dirs(directory, progress, progress_bar):
    """
    Loops through each first level sub directory in a specified directory and returns a pandas dataframe a row for each 
    sub directory containing:
    - the sub directory name
    - the name of the most recently edited file in that sub directory
    - the date the file was modified
    Returns the output as a pandas dataframe
    Also updates progress, a tkinter ProgressBar
    """
    list_folders_dates = []
    progress.set(0)
    progress_bar.update_idletasks()
    max_count = more_itertools.ilen(Path(directory).iterdir())
    for path in Path(directory).iterdir():
        progress.set(progress.get() + (100/max_count))
        progress_bar.update_idletasks()
        if path.is_dir():
            try:
                time, file_path = max((f.stat().st_mtime, f) for f in path.iterdir() if f.is_file() and f.name != 'Thumbs.db')
                list_folders_dates.append([file_path.parent.stem, file_path.name, datetime.fromtimestamp(time)])
            except:
                list_folders_dates.append([path.stem, 'No file', ])
    return pd.DataFrame(list_folders_dates,columns=['Folder','File name','Date last modified']).sort_values(by=['Date last modified'])