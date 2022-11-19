import tkinter as tk
from tkinter import *
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from tkinter import filedialog as fd
from tkinter import messagebox as mb


def open_file():
    global file_path
    file_path = fd.askopenfilename()
    if file_path:
        open_btn.config(state='normal')
    else:
        mb.showinfo("Alert!", "you have not selected a file")


def posting():
    option = webdriver.ChromeOptions()
    #option.add_argument(f"user-agent={UserAgent}")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.headless = False
    driver = webdriver.Chrome(
        executable_path=r"chrome\chromedriver.exe",
        options=option)
    driver.get("https://facebook.com")
    auth_btn = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]").click()
    email_input = driver.find_element(By.ID, "email")
    email_input.clear()
    email_input.send_keys(login_entry.get())
    password_input = driver.find_element(By.ID, "pass")
    password_input.clear()
    password_input.send_keys(password_entry.get())
    login_btn = driver.find_element(By.XPATH,
                                    "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button").click()
    time.sleep(3)

    # sending
    visited_group = set()
    try:
        with open(file_path) as f:
            for link in f:
                if link in visited_group:
                    info = (f"The link ({link}) to the group in your .txt file is repeated")
                    mb.showinfo("Link!", info)
                    continue
                visited_group.add(link)
                driver.get(link)
                label_process_link['text'] = str(link)
                time.sleep(3)
                try:
                    span = driver.find_element(By.XPATH, "//*[contains(text(), 'Napisz coś...')]")
                    parent_1 = span.find_element(By.XPATH, "..")
                    parent_2 = parent_1.find_element(By.XPATH, "..")
                    parent_2.click()
                    time.sleep(2)
                    actiounchains = ActionChains(driver)
                    actiounchains.send_keys(text_txt.get('1.0', 'end'))
                    actiounchains.send_keys(Keys.TAB * 8)
                    actiounchains.perform()
                    time.sleep(2)
                    actiounchains.send_keys(Keys.ENTER)
                    actiounchains.perform()
                    time.sleep(6)
                except:
                    continue
    except Exception:
        driver.close()
        driver.quit()
        mb.showerror("Something wrong!", "You may not have chosen the path to the text file")
    finally:
        f.close()
        driver.close()
        driver.quit()
        mb.showinfo("Info", "Success!")


def help_me():
    mb.showinfo("Important info!", """Before clicking on the green button, make sure you have entered the correct details of 
your facebook account. Then, by clicking on the "Open file" button, specify the path to the text file with the list of 
groups in the format: "https://www.facebook.com/groups/123456789/", which you prepared in advance.
The field named "Text" must not have "unusual" characters, such as emoticons.""")


# main
win = tk.Tk()
win.title("Rekruter helper")
win.geometry("330x250")
win.resizable(False, False)

# labels
label_text = tk.Label(win, text="Text")
label_login = tk.Label(win, text="Login")
label_password = tk.Label(win, text="Password")
label_process_link = tk.Label(win, text="Link:")

# buttons
posting_btn = tk.Button(win, text="Start posting!", command=posting, bg="green")
open_btn = tk.Button(win, text="Open file", command=open_file)
help_btn = tk.Button(win, text="Help", command=help_me)
stop_posting_btn = tk.Button(win, text="Stop posting", command=win.destroy, bg="red")

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
label_text.grid(row=3, column=0, sticky="n")
text_txt.grid(row=3, column=1)
password_entry.grid(row=1, column=1, sticky="w")
posting_btn.grid(row=0, column=2, sticky="we")
open_btn.grid(row=3, column=2, sticky="we")
stop_posting_btn.grid(row=1, column=2, sticky="we")
help_btn.grid(row=4, column=2, sticky="we")
label_process_link.grid(row=4, column=0, columnspan=3, sticky="w")

win.mainloop()