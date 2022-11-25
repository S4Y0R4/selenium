import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import threading
import poster as p


def file_dialog_wrapper(on_open_file):
    file_path = fd.askopenfilename(filetypes=[("Text files", ".txt")])
    on_open_file(file_path)


class AutoPosterGUI(threading.Thread):
    def __init__(self, poster: p.Poster):
        threading.Thread.__init__(self)
        self.posting_btn = None
        self.stop_posting_btn = None
        self.open_btn = None
        self.auth_btn = None
        self.label_login = None
        self.label_password = None
        self.label_text = None
        self.password_entry = None
        self.text_txt = None
        self.login_entry = None
        self.win = None
        self.poster = poster
        self.start()

    def run(self) -> None:
        self.win = tk.Tk()
        self.login_entry = tk.Entry(self.win, width=29)
        self.label_password = tk.Label(self.win, text="Password")
        self.auth_btn = tk.Button(self.win, text="Authentication",
                                  command=lambda: threading.Thread(
                                      target=self.poster.handle_login(self.login_entry.get(),
                                                                      self.password_entry.get()), daemon=True).start())

        self.text_txt = tk.Text(self.win, width=22, height=10, wrap=WORD)
        self.help_btn = tk.Button(self.win, text="Help", command=self.how_to_use)
        self.label_text = tk.Label(self.win, text="Text")
        self.password_entry = tk.Entry(self.win, width=29, show="*")
        self.label_login = tk.Label(self.win, text="Login")
        self.stop_posting_btn = tk.Button(self.win, text="Stop posting", command=self.stop_execution, bg="red")

        self.posting_btn = tk.Button(self.win, text="Start posting!",
                                     command=lambda: threading.Thread(target=self.start_posting,
                                                                      daemon=True).start())

        self.open_btn = tk.Button(self.win, text="Open file",
                                  command=lambda: file_dialog_wrapper(on_open_file=self.poster.handle_open_file))
        self.label_group = tk.Label(self.win)

        self.setup_gui()

    def stop_execution(self):
        if self.poster.is_posting:
            self.poster.stop_execution()

    def start_posting(self):
        if not self.poster.is_driver_online or self.poster.is_posting:
            self.poster.stop_execution()
            self.poster.start_driver()
            self.poster.handle_login()

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
        self.create_bottom_part()
        self.win.mainloop()

    def create_body(self):
        self.label_text.grid(row=2, column=0, sticky="n")
        self.text_txt.grid(row=2, column=1)
        self.open_btn.grid(row=2, column=2, sticky="we")


    def create_bottom_part(self):
        self.help_btn.grid(row=3, column=2, sticky="we")
        self.label_group.grid(row=4, column=0, columnspan=3, sticky="we")


    def create_login_component(self):
        self.label_login.grid(row=0, column=0)
        self.label_password.grid(row=1, column=0)
        self.login_entry.grid(row=0, column=1, sticky="w")
        self.password_entry.grid(row=1, column=1, sticky="w")
        self.auth_btn.grid(row=0, column=2, rowspan=2, sticky="sn")

    def handle_posting_started(self):
        print('posting started', self)

    def how_to_use(self):
        info = """Before clicking on the green button, make sure you have entered the correct details of your facebook account. Then, by clicking on the "Open file" button, specify the path to the text file with the list of groups in the format: "https://www.facebook.com/groups/123456789/", which you prepared in advance. The field named "Text" must not have "unusual" characters, such as emoticons."""
        return mb.showinfo("Information", info)

    def handle_link_changed(self, group: str):
        self.label_group['text'] = group

    def handle_logged_in(self):
        self.posting_btn.grid(row=0, column=3, sticky="we")
        self.stop_posting_btn.grid(row=1, column=3, sticky="we")

    def status_switch_posting_btn(self):
        if self.poster.is_posting:
            return self.posting_btn.config(state="disabled")
        else:
            return self.posting_btn.config(state="normal")

    def status_switch_stop_posting_btn(self):
        if self.poster.is_posting:
            return self.stop_posting_btn.config(state="disabled")
        else:
            return self.stop_posting_btn.config(state="normal")

    def status_switch_auth_btn(self):
        if self.poster.is_logged_in():
            return self.auth_btn.config(state="disabled")
        else:
            return self.auth_btn.config(state="normal")