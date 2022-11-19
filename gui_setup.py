import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
import threading
import poster as p


def file_dialog_wrapper(on_open_file):
    file_path = fd.askopenfilename()
    on_open_file(file_path)


class AutoPosterGUI(threading.Thread):
    def __init__(self, poster: p.Poster):
        threading.Thread.__init__(self)
        self.posting_btn = None
        self.stop_posting_btn = None
        self.open_btn = None
        self.label_login = None
        self.password_entry = None
        self.label_text = None
        self.text_txt = None
        self.auth_btn = None
        self.label_password = None
        self.login_entry = None
        self.win = None
        self.poster = poster
        self.start()

    def run(self) -> None:
        self.win = tk.Tk()
        self.login_entry = tk.Entry(self.win, width=29)
        self.label_password = tk.Label(self.win, text="Password")
        self.auth_btn = tk.Button(self.win, text="Authentication",
                                  command=lambda: self.poster.handle_login(self.login_entry.get(),
                                                                           self.password_entry.get()))

        self.text_txt = tk.Text(self.win, width=22, height=10, wrap=WORD)
        self.label_text = tk.Label(self.win, text="Text")
        self.password_entry = tk.Entry(self.win, width=29, show="*")
        self.label_login = tk.Label(self.win, text="Login")
        self.stop_posting_btn = tk.Button(self.win, text="Stop posting", command=self.stop_execution, bg="red")

        self.posting_btn = tk.Button(self.win, text="Start posting!",
                                     command=lambda: threading.Thread(target=self.start_posting,
                                                                      daemon=True).start())

        self.open_btn = tk.Button(self.win, text="Open file",
                                  command=lambda: file_dialog_wrapper(on_open_file=self.poster.handle_open_file))
        self.setup_gui()

    def stop_execution(self):
        if self.poster.is_posting:
            self.poster.stop_execution()

    def start_posting(self):
        if not self.poster.is_driver_online:
            self.poster.start_driver()
            self.poster.handle_login()
        if self.poster.is_posting:
            self.poster.stop_execution()

        self.poster.start_posting(self.text_txt.get('1.0', 'end'))

    def callback(self):
        self.poster.stop_execution()
        self.win.quit()

    def setup_gui(self):
        self.win.title("Recruiter helper")
        self.win.geometry("430x280")
        self.win.resizable(False, False)
        self.create_login_component()
        self.create_body()
        self.win.mainloop()

    def create_body(self):
        self.label_text.grid(row=3, column=0, sticky="n")
        self.text_txt.grid(row=3, column=1)
        self.open_btn.grid(row=3, column=2, sticky="we")

    def create_login_component(self):
        self.label_login.grid(row=0, column=0)
        self.label_password.grid(row=1, column=0)
        self.login_entry.grid(row=0, column=1, sticky="w")
        self.password_entry.grid(row=1, column=1, sticky="w")
        self.auth_btn.grid(row=0, column=2, rowspan=2, sticky="sn")

    def handle_posting_started(self):
        print('posting started', self)

    def handle_link_changed(self, group: str):
        print('link changed ' + group, self)

    def handle_logged_in(self):
        self.posting_btn.grid(row=0, column=3, sticky="we")
        self.stop_posting_btn.grid(row=1, column=3, sticky="we")
