import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from pathlib import Path

from folder_last_updated_alg import latest_update_to_sub_dirs

program_title = 'Latest CV finder'

class App(tk.Tk):

    def __init__(self, program_title):
        tk.Tk.__init__(self)

        self.title(program_title)

        # the container is where we'll stack our frames on top of each other, then the one we want visible will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WelcomeScreen, ProgressBar):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame('WelcomeScreen')

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomeScreen(tk.Frame):

    def __init__(self, parent, controller):
        """
        Welcome screen
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        header_label = ttk.Label(self, text='Find the most recently edited file in each folder')
        filepath_label = ttk.Label(self, text='Filepath: ')
        filepath_entry = ttk.Entry(self, width=50)
        browse_button = ttk.Button(self, text="Browse", command=partial(self.browse_directory, filepath_entry))
        run_button = ttk.Button(self, text="Run", command=partial(self.run_algorithm, filepath_entry))  

        header_label.grid(row=0, column=0, columnspan=2, sticky='W')
        filepath_label.grid(row=1, column=0, sticky='W')
        filepath_entry.grid(row=1, column=1)
        browse_button.grid(row=1, column=2)
        run_button.grid(row=2, column=2)

    def browse_directory(self, entry):
        """
        Browse the file system and select a directory
        """
        dir_path = filedialog.askdirectory(title='Choose a folder location')
        if dir_path != None:
            entry.delete(0, tk.END)
            entry.insert(0, dir_path)

    def run_algorithm(self, entry):
        self.controller.show_frame('ProgressBar')
        self.controller.update()
        progress_bar = self.controller.frames['ProgressBar']
        latest_files = latest_update_to_sub_dirs(entry.get(), progress_bar.progress_bar_var, progress_bar)
        try:
            save_location = tk.filedialog.asksaveasfilename(title='Choose a save location',defaultextension='.xlsx')
            latest_files.to_excel(save_location, index=False)
        except:
            pass
        self.controller.show_frame('WelcomeScreen')

class ProgressBar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        header_label = ttk.Label(self, text="Progress: ")
        
        self.progress_bar_var = tk.DoubleVar()
        self.progress_bar_var.set(0)
        progress_bar = ttk.Progressbar(self, orient='horizontal', length=350, variable=self.progress_bar_var, mode='determinate')

        header_label.grid(row=0, column=0, sticky='W')
        progress_bar.grid(row=1, column=1)

if __name__ == "__main__":
    app = App(program_title)
    app.mainloop()