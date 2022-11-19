import time
from tkinter import messagebox as mb

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

WRITE_SOMETHING_PATH = "//*[contains(text(), 'Napisz coś...')]"

LOGIN_BUTTON_PATH = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button"

COOKIE_BUTTON_PATH = "/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]"

HOME_BUTTON_PATH = "/html/body/div[1]/div/div[1]/div/div[3]/div[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/div[" \
                   "1]/span/div/a/i "


class Poster:
    def __init__(self):
        self.is_posting = False
        self.is_driver_online = False
        self.gui = None
        self.links = set()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-notifications")
        self.options.headless = False
        self.current_driver = None
        self.gui = None

    def start_driver(self):
        self.current_driver = webdriver.Chrome(
            executable_path=r"chrome\chromedriver.exe",
            options=self.options)
        self.is_driver_online = True
        self.current_driver.get("https://facebook.com")

    def bind_gui(self, gui):
        self.gui = gui

    def handle_login(self, login: str, password: str):
        print(self)
        self.auth("+48 794 506 479", "Anime13!")

    def handle_open_file(self, file):
        self.get_groups_from_file(file)

    def stop_execution(self):
        self.is_posting = False
        self.current_driver.quit()
        self.is_driver_online = False

    def auth(self, login, password) -> None:
        self.current_driver.find_element(By.XPATH, COOKIE_BUTTON_PATH).click()
        email_input = self.current_driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys(login)
        password_input = self.current_driver.find_element(By.ID, "pass")
        password_input.clear()
        password_input.send_keys(password)
        self.current_driver.find_element(By.XPATH, LOGIN_BUTTON_PATH).click()

        if not self.is_logged_in():
            mb.showinfo("Attention!", "Your username or password is incorrect")
            return

        self.gui.handle_logged_in()

    def get_groups_from_file(self, file_path):
        self.links = set()
        with open(file_path) as file:
            for link in file:
                self.links.add(link)

    def is_logged_in(self) -> bool:
        try:
            home_button = self.current_driver.find_element(By.XPATH, HOME_BUTTON_PATH)
            print(home_button.get_attribute("data-visualcompletion"))
            return home_button.get_attribute("data-visualcompletion") == "css-img"
        except:
            return False

    def write_message(self, message: str):
        action_chain = ActionChains(self.current_driver)
        action_chain.send_keys(message)
        action_chain.send_keys(Keys.TAB * 8)
        action_chain.perform()
        time.sleep(2)
        action_chain.send_keys(Keys.ENTER)
        action_chain.perform()

    @staticmethod
    def get_click_able_button(span: WebElement) -> WebElement:
        parent = span.find_element(By.XPATH, "..")
        return parent.find_element(By.XPATH, "..")

    def start_posting(self, message_to_post):
        self.is_posting = True
        assert (len(self.links) > 0)
        self.gui.handle_posting_started()
        for group in self.links:
            self.current_driver.get(group)
            self.gui.handle_link_changed(group)
            time.sleep(3)  # TODO: change it to await result, sleep for HOBOS
            try:

                write_something = self.current_driver.find_element(By.XPATH, WRITE_SOMETHING_PATH)
                button = self.get_click_able_button(write_something)
                button.click()
                time.sleep(2)
                self.write_message(message_to_post)
                time.sleep(6)
            except Exception as e:
                print(e)
                continue
