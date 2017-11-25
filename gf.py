import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from domain import *
from queue import Queue
from spider import Spider
import threading
from general import file_to_set


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
        for F in (MainPage, History, WaitList):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            if F == History:
                frame.hist_text.insert(tk.END, 'Hello World')
                frame.hist_text.config(state='disabled')
            if F == WaitList:
                frame.wait_text.insert(tk.END, 'Nothing')

        menu = tk.Menu(self)
        home_menu = tk.Menu(menu)
        hist_menu = tk.Menu(menu)
        wait_menu = tk.Menu(menu)
        home_menu.add_command(label='HomePage', command=lambda: self.display_frame(MainPage))
        hist_menu.add_command(label='Show', command=lambda: self.display_frame(History))
        wait_menu.add_command(label='Show', command=lambda: self.display_frame(WaitList))
        menu.add_cascade(label='Home', menu=home_menu)
        menu.add_cascade(label='History', menu=hist_menu)
        menu.add_cascade(label='Queue', menu=wait_menu)

        self.config(menu=menu)
        self.display_frame(MainPage)

    def display_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class MainPage(tk.Frame):

    THREADS_NUMBER = 0
    PROJECT_NAME = ''
    START_URL = ''
    DOMAIN_NAME = ''
    QUEUE_FILE = ''
    CRAWLED_FILE = ''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.queue = None

        buttons_frame = ttk.Frame(self)
        entry_frame = ttk.Frame(self)
        buttons_frame.grid(row=1, column=1, sticky='nesw')
        entry_frame.grid(row=0, column=0, sticky='nw')

        thread_label = ttk.Label(entry_frame, text='Number of threads:', font=LARGE_FONT)
        thread_label.grid(row=1, column=0)
        start_label = ttk.Label(entry_frame, text='Enter the main URL:', font=LARGE_FONT)
        start_label.grid(row=0, column=0)
        project_name_label = ttk.Label(entry_frame, text='Project Name:', font=LARGE_FONT)
        project_name_label.grid(row=2, column=0)

        self.thread_entry = ttk.Entry(entry_frame)
        self.thread_entry.grid(row=1, column=1)
        self.start_entry = ttk.Entry(entry_frame)
        self.start_entry.grid(row=0, column=1)
        self.project_name_entry = ttk.Entry(entry_frame)
        self.project_name_entry.grid(row=2, column=1)

        start_button = ttk.Button(buttons_frame, text='Start', command=self.initialize)
        start_button.grid(row=0, column=0, sticky='nsew')
        stop_button = ttk.Button(buttons_frame, text='Stop')
        stop_button.grid(row=0, column=1, sticky='nsew')

    def initialize(self):
        try:
            MainPage.THREADS_NUMBER = int(self.thread_entry.get())
        except:
            tk.messagebox.showinfo("Warning!", "Please enter an integer in Number of threads box")

        MainPage.PROJECT_NAME = self.project_name_entry.get()
        MainPage.PROJECT_NAME = MainPage.PROJECT_NAME.strip().lower()
        MainPage.START_URL = self.start_entry.get()
        MainPage.START_URL = MainPage.START_URL.strip().lower()

        if MainPage.START_URL =='' or MainPage.PROJECT_NAME == '':
            tk.messagebox.showinfo("Warning!", "Please fill ALL the entry boxes")
        MainPage.DOMAIN_NAME = get_domain_name(MainPage.START_URL)
        MainPage.QUEUE_FILE = MainPage.PROJECT_NAME + "/queue.txt"
        MainPage.CRAWLED_FILE = MainPage.PROJECT_NAME + "/crawled.txt"
        self.startt()

    def startt(self):
        self.queue = Queue()
        Spider(MainPage.PROJECT_NAME, MainPage.START_URL, MainPage.DOMAIN_NAME)
        self.create_workers()
        self.crawl()
    
    def create_workers(self):
        for _ in range(MainPage.THREADS_NUMBER):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()

    def work(self):
        while True:
            url = self.queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            self.queue.task_done()

    def create_jobs(self):
        for link in file_to_set(MainPage.QUEUE_FILE):
            self.queue.put(link)
        self.queue.join()
        self.crawl()

    def crawl(self):
        queue_links = file_to_set(MainPage.QUEUE_FILE)
        if len(queue_links) > 0:
            print(str(len(queue_links)) + 'links in the queue')
            self.create_jobs()


class History(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        text_frame = ttk.Frame(self)
        text_frame.pack()
        label = ttk.Label(text_frame, text='The last 100 URLs', font=LARGE_FONT)
        label.pack()
        self.hist_text = tk.Text(text_frame)
        self.hist_text.pack()


class WaitList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        text_frame = ttk.Frame(self)
        text_frame.pack()
        label = ttk.Label(text_frame, text='The next 100 URLs that are waiting to be crawled', font=LARGE_FONT)
        label.pack()
        self.wait_text = tk.Text(text_frame)
        self.wait_text.pack()

app = App()

app.mainloop()

