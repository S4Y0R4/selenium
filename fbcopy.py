import threading
import tkinter as tk
from tkinter import *
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tkinter import filedialog as fd
from tkinter import messagebox as mb


def auth():
    while thread_stop == False:
        email_input = driver_global.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys(login_entry.get())
        password_input = driver_global.find_element(By.ID, "pass")
        password_input.clear()
        password_input.send_keys(password_entry.get())
        driver_global.find_element(By.XPATH,
                            "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button").click()
        try:
            driver_global.find_element(By.XPATH, "//*[contains(text(), 'Zapamiętaj hasło')]")
            posting_btn.grid(row=0, column=3, sticky="we")
            stop_posting_btn.grid(row=1, column=3, sticky="we")
        except:
            driver_global.get("https://facebook.com")
            mb.showinfo("Attention!", "Your username or password is incorrect")
            auth_btn.config(state="normal")
        return
    else:
        driver_global.get("https://facebook.com")
        return mb.showinfo("Info", "Work has been stopped.")


def open_file():
    global file_path
    file_path = fd.askopenfilename()


def stop_posting():
    global thread_stop
    thread_stop = True


def on_buttons():
    text_txt.config(state="normal")
    login_entry.config(state="normal")
    password_entry.config(state="normal")
    open_btn.config(state="normal")
    posting_btn.config(state="normal")
    auth_btn.config(state="normal")


def off_buttons():
    auth_btn.config(state="disabled")
    text_txt.config(state="disabled")
    login_entry.config(state="disabled")
    password_entry.config(state="disabled")
    open_btn.config(state="disabled")
    posting_btn.config(state="disabled")

def stop_execution():
    driver.close()
    driver.quit()
    print(threading.active_count())

def posting():
    if not is_driver_active():
        driver_global = driver_setup()
    thread_stop = False
    option_global.headless = False
    off_buttons()
    visited_group = set()
    try:
        while thread_stop == False:
            with open(file_path) as f:
                for link in f:
                    if link in visited_group:
                        info = (f"The link ({link}) to the group in your .txt file is repeated")
                        mb.showinfo("Link!", info)
                        continue
                    visited_group.add(link)
                    driver_global.get(link)
                    label_process_link['text'] = "Link: " + str(link)
                    time.sleep(3)
                    try:
                        span = driver_global.find_element(By.XPATH, "//*[contains(text(), 'Napisz coś...')]")
                        parent_1 = span.find_element(By.XPATH, "..")
                        parent_2 = parent_1.find_element(By.XPATH, "..")
                        parent_2.click()
                        #WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div/div/span/br"))
                        time.sleep(2)
                        actiounchains = ActionChains(driver_global)
                        actiounchains.send_keys(text_txt.get('1.0', 'end'))
                        actiounchains.send_keys(Keys.TAB * 8)
                        actiounchains.perform()
                        time.sleep(2)
                        actiounchains.send_keys(Keys.ENTER)
                        actiounchains.perform()
                        time.sleep(6)
                    except:
                        continue
            mb.showinfo("Info", "Success!")
        else:
            mb.showinfo("Info", "Work has been stopped")
    except OSError:
        mb.showwarning("File not found", "Specify the path to the file")
    except NameError:
        mb.showwarning("File not found", "Specify the path to the file")
    #except NoSuchWindowException:
        #mb.showwarning("Сritical error", "The driver window was closed")
    #except Exception as ex:
        #print(ex)
    finally:
        label_process_link['text'] = "Link:"
        on_buttons()
        return


def help_me():
    mb.showinfo("Important info!", """Before clicking on the green button, make sure you have entered the correct details of 
your facebook account. Then, by clicking on the "Open file" button, specify the path to the text file with the list of 
groups in the format: "https://www.facebook.com/groups/123456789/", which you prepared in advance.
The field named "Text" must not have "unusual" characters, such as emoticons.""")

def driver_setup():
    option = webdriver.ChromeOptions()
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("--disable-notifications")
    option.headless = False
    driver = webdriver.Chrome(
        executable_path=r"chrome\chromedriver.exe",
        options=option)
    driver.get("https://facebook.com")
    driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]").click()
    return driver

def is_driver_active():
    return get_status(driver_global) == "Alive"

def get_status(driver):
    try:
        driver.execute(Command.STATUS)
        return "Alive"
    except Exception as ex:
        return "Dead"

# main
global driver_global
driver_global = driver_setup()
global option_global
thread_stop = False
win = tk.Tk()
win.title("Rekruter helper")
win.geometry("430x280")
win.resizable(False, False)

# labels
label_text = tk.Label(win, text="Text")
label_login = tk.Label(win, text="Login")
label_password = tk.Label(win, text="Password")
label_process_link = tk.Label(win, text="Link:")

# buttons
posting_btn = tk.Button(win, text="Start posting!",
                        command=(lambda: threading.Thread(target=posting, daemon=True).start()), bg="green")
stop_posting_btn = tk.Button(win, text="Stop posting", command=stop_execution, bg="red")
auth_btn = tk.Button(win, text="Authentication", command=lambda: threading.Thread(target=auth, daemon=True).start())
open_btn = tk.Button(win, text="Open file", command=open_file)
help_btn = tk.Button(win, text="Help", command=help_me)

# Text
groups_txt = tk.Text(win, width=48, height=5, wrap=WORD)
text_txt = tk.Text(win, width=22, height=10, wrap=WORD)

# entry
login_entry = tk.Entry(win, width=29)
password_entry = tk.Entry(win, width=29, show="*")
path_entry = tk.Entry(win, width=29)

# grids
label_login.grid(row=0, column=0)
login_entry.grid(row=0, column=1, sticky="w")
label_password.grid(row=1, column=0)
password_entry.grid(row=1, column=1, sticky="w")
label_text.grid(row=3, column=0, sticky="n")
text_txt.grid(row=3, column=1)
open_btn.grid(row=3, column=2, sticky="we")
help_btn.grid(row=4, column=2, sticky="we")
label_process_link.grid(row=5, column=0, columnspan=4, sticky="w")
auth_btn.grid(row=0, column=2, rowspan=2, sticky="sn")

win.mainloop()
