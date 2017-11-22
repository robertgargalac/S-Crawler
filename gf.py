import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "S-Crawler")
        self.geometry('600x600')

        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, History):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            if F == History:
                frame.hist_text.insert(tk.END, 'Hello World')
                frame.hist_text.config(state='disabled')

        menu = tk.Menu(self)
        home_menu = tk.Menu(menu)
        hist_menu = tk.Menu(menu)
        home_menu.add_command(label='HomePage', command=lambda: self.display_frame(MainPage))
        hist_menu.add_command(label='Show', command=lambda: self.display_frame(History))
        menu.add_cascade(label='Home', menu=home_menu)
        menu.add_cascade(label='History', menu=hist_menu)

        self.config(menu=menu)
        self.display_frame(MainPage)

    def display_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        buttons_frame = ttk.Frame(self)
        entry_frame = ttk.Frame(self)
        buttons_frame.grid(row=1, column=1, sticky='nesw')
        entry_frame.grid(row=0, column=0, sticky='nw')

        thread_label = ttk.Label(entry_frame, text='Number of threads:', font=LARGE_FONT)
        thread_label.grid(row=1, column=0)
        start_label = ttk.Label(entry_frame, text='Enter the main URL:', font=LARGE_FONT)
        start_label.grid(row=0, column=0)

        thread_entry = ttk.Entry(entry_frame)
        thread_entry.grid(row=1, column=1)
        start_entry = ttk.Entry(entry_frame)
        start_entry.grid(row=0, column=1)

        start_button = ttk.Button(buttons_frame, text='Start')
        start_button.grid(row=0, column=0, sticky='nsew')
        stop_button = ttk.Button(buttons_frame, text='Stop')
        stop_button.grid(row=0, column=1, sticky='nsew')


class History(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        text_frame = ttk.Frame(self)
        text_frame.pack()
        label = ttk.Label(text_frame, text='The last 100 URLs', font=LARGE_FONT)
        label.pack()
        self.hist_text = tk.Text(text_frame)
        self.hist_text.pack()

app = App()
app.mainloop()

