from tkinter import filedialog as fd
from tkinter import messagebox as mb
import threading
import poster as p
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


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
        self.password_entry = None
        self.text_txt = None
        self.login_entry = None
        self.win = None
        self.poster = poster
        self.help_btn = None
        self.text_txt = None
        self.label_group = None
        self.path_to_file_label = None
        self.start()

    def run(self) -> None:
        self.win = customtkinter.CTk()  # create CTk window like you do with the Tk window
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.login_entry = customtkinter.CTkEntry(master=self.win, placeholder_text="Your login or number", width=200)
        self.auth_btn = customtkinter.CTkButton(master=self.win, text="Authentication", width=100,
                                                command=lambda: threading.Thread(
                                                    target=self.poster.handle_login(self.login_entry.get(),
                                                                                    self.password_entry.get()),
                                                    daemon=True).start())

        self.help_btn = customtkinter.CTkButton(master=self.win, text="Help me!", width=100, command=self.how_to_use())
        # self.label_text = tk.Label(self.win, text="Text")
        self.password_entry = customtkinter.CTkEntry(master=self.win, placeholder_text="Your password", width=200,
                                                     show="*")
        self.stop_posting_btn = customtkinter.CTkButton(master=self.win, text="Stop posting!", width=100,
                                                        command=self.stop_execution)

        self.posting_btn = customtkinter.CTkButton(master=self.win, text="Start posting!", width=100,
                                                   command=lambda: threading.Thread(target=self.start_posting,
                                                                                    daemon=True).start())

        self.open_btn = customtkinter.CTkButton(master=self.win, text="Open file", width=100,
                                                command=lambda: file_dialog_wrapper(
                                                    on_open_file=self.poster.handle_open_file))
        self.label_group = customtkinter.CTkLabel(master=self.win, text="The link for the processed group will be here")
        self.text_txt = customtkinter.CTkTextbox(master=self.win, width=310)
        self.path_to_file_label = customtkinter.CTkLabel(master=self.win, text="The path to your txt file will be here")
        self.setup_gui()

    def stop_execution(self):
        if self.poster.is_posting:
            self.poster.stop_execution()

    def start_posting(self):
        if not self.poster.is_posting:
            self.poster.stop_execution()
        message = self.text_txt.get("0.0", "end")
        self.poster.start_posting(message)

    def callback(self):
        self.poster.stop_execution()
        self.win.quit()

    def setup_gui(self):
        self.win.title("Recruiter helper")
        self.win.geometry("450x350")
        self.win.resizable(False, False)
        self.create_login_component()
        self.create_body()
        self.win.mainloop()

    def create_body(self):
        self.text_txt.grid(row=2, column=0, sticky="nw", padx=5, pady=5, columnspan=2)
        self.open_btn.grid(row=2, column=2, sticky="nw", padx=5, pady=5)
        self.help_btn.grid(row=4, column=2, padx=5, pady=5)
        self.label_group.grid(row=3, column=0, sticky="nw", padx=5, pady=5, columnspan=2)
        self.path_to_file_label.grid()

    def create_login_component(self):
        self.login_entry.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.password_entry.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.auth_btn.grid(row=0, column=1, padx=5, pady=5, rowspan=2, sticky="ns")

    def handle_path_to_file(self):
        self.label_group.configure(text=self)

    def handle_posting_started(self):
        print('posting started', self)

    @staticmethod
    def how_to_use() -> str:
        info = """Before clicking on the green button, make sure you have entered the correct details of your facebook \
        account. Then, by clicking on the "Open file" button, specify the path to the text file with the list of groups\
         in the format: "https://www.facebook.com/groups/123456789/", which you prepared in advance. The field named \
         'Text' must not have "unusual" characters, such as emoticons."""
        return mb.showinfo("Information", info)

    def handle_link_changed(self, group: str):
        self.label_group.configure(text=group)

    def handle_logged_in(self):
        self.posting_btn.grid(row=0, column=2, padx=5, pady=5)
        self.stop_posting_btn.grid(row=1, column=2, padx=5, pady=5)

    def status_switch_posting_btn(self):
        if self.poster.is_posting:
            self.posting_btn.configure(state="disabled")
        else:
            self.posting_btn.configure(state="normal")

    def status_switch_stop_posting_btn(self):
        if self.poster.is_posting:
            self.stop_posting_btn.configure(state="normal")
        else:
            self.stop_posting_btn.configure(state="disabled")

    def status_switch_auth_btn(self):
        self.auth_btn.configure(state="disabled")

    def status_switch_open_btn(self):
        if self.poster.is_posting:
            self.open_btn.configure(state="disabled")
        else:
            self.open_btn.configure(state="normal")

    def on_closing(self):
        if mb.askokcancel("Quit", "Do you want to quit?"):
            self.poster.current_driver.quit()
            self.win.destroy()
