import collections
import time
from tkinter import messagebox as mb
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

COOKIE_BUTTON_PATH = "/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]"

LOGIN_BUTTON_PATH = "/html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/form/div/div[3]/button"

HOME_BUTTON_PATH = "/html/body/div[1]/div/div[1]/div/div[3]/div[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/div[" \
                   "1]/span/div/a/i"

PICTURE_BUTTON_PATH = "/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div/d" \
                      "iv[3]/div/div[2]/div/div/div/div[2]/div[2]/div[1]/span[1]/i"

WRITE_SOMETHING_PATH = "//*[contains(text(), 'Napisz coś...')]"

PEOPLE_BUTTON_PATH = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/" \
                     "div/div[1]/div/div/div[1]/div/div[3]/div[1]/div" \
                     "[2]/div[4]/div/span/div/div/div[1]/div/div/div[1]/i"
GROUP_NAME_BUTTON = "_"


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

    def start_driver(self):
        self.current_driver = webdriver.Chrome(
            executable_path=r"chrome\chromedriver.exe",
            options=self.options)
        self.is_driver_online = True
        self.home_page()

    def bind_gui(self, gui):
        self.gui = gui

    def handle_login(self, login: str, password: str):
        self.auth(login, password)

    def handle_open_file(self, file):
        self.set_groups_from_file(file)

    def stop_execution(self):
        self.is_posting = False
        self.current_driver.quit()
        self.is_driver_online = False

    def auth(self, login, password) -> None:

        if self.is_cookie_button_exist():
            self.current_driver.find_element(By.XPATH, COOKIE_BUTTON_PATH).click()

        email_input = self.current_driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys(login)
        password_input = self.current_driver.find_element(By.ID, "pass")
        password_input.clear()
        password_input.send_keys(password)
        self.current_driver.find_element(By.NAME, "login").click()

        if not self.is_logged_in():
            mb.showinfo("Warning!", "Your login or password is incorrect")
            self.home_page()
            return

        self.gui.handle_logged_in()

    def is_logged_in(self) -> bool:

        if self.is_home_button_exist():
            home_button = self.current_driver.find_element(By.XPATH, HOME_BUTTON_PATH)
            if home_button.get_attribute("data-visualcompletion") == "css-img":
                return True
        elif self.is_picture_button_exist():
            picture_button = self.current_driver.find_element(By.XPATH, PICTURE_BUTTON_PATH)
            if picture_button.get_attribute("data-visualcompletion") == "css-img":
                return True
        else:
            return False

    def is_home_button_exist(self):
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, HOME_BUTTON_PATH)))
            print("HOME_BUTTON was found")
            return True
        except TimeoutException:
            print("HOME_BUTTON was not found")
            return False

    def is_picture_button_exist(self):
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, PICTURE_BUTTON_PATH)))
            print("PICTURE_BUTTON was found")
            return True
        except TimeoutException:
            print("PICTURE_BUTTON was not found")
            return False

    def is_cookie_button_exist(self) -> bool:
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, COOKIE_BUTTON_PATH)))
            print("COOKIE_BUTTON was found")
            return True
        except TimeoutException:
            print("COOKIE_BUTTON was not found")
            return False

    def is_text_field_in_group_exist(self):
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, PEOPLE_BUTTON_PATH)))
            print("PEOPLE_BUTTON was found")
            return True
        except TimeoutException:
            print("PEOPLE_BUTTON was not found")
            return False

    def home_page(self):
        self.current_driver.get("https://facebook.com")

    @staticmethod
    def is_file_path_not_empty(file_path):

        if len(file_path) > 0:
            return True

    def set_groups_from_file(self, file_path):

        if self.is_file_path_not_empty(file_path):
            self.links = set()
            with open(file_path) as file:
                for link in file:
                    self.links.add(link)
                file.close()

    @staticmethod
    def count_lines(message: str):
        counter = collections.Counter(message)
        num_of_new_line = counter["\n"]
        return num_of_new_line

    def write_message(self, message: str):
        action_chain = ActionChains(self.current_driver)
        action_chain.send_keys(message)
        if self.count_lines(message) > 3:
            action_chain.send_keys(Keys.TAB * 8)
        else:
            action_chain.send_keys(Keys.TAB * 9)
        action_chain.perform()
        time.sleep(1)
        action_chain.send_keys(Keys.ENTER)
        action_chain.perform()

    @staticmethod
    def get_clickable_button(span: WebElement) -> WebElement:
        parent = span.find_element(By.XPATH, "..")
        return parent.find_element(By.XPATH, "..")

    def is_length_of_links_more_than_0(self):
        if len(self.links) > 0:
            return True

    def is_write_something_exist(self):
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, WRITE_SOMETHING_PATH)))
            print("WRITE_SOMETHING_PATH was found")
            return True
        except TimeoutException:
            print("WRITE_SOMETHING_PATH was not found")
            return False

    def start_posting(self, message_to_post):
        self.is_posting = True
        if self.is_length_of_links_more_than_0():
            self.gui.handle_posting_started()
            for group in self.links:
                self.current_driver.get(group)
                self.gui.handle_link_changed(group)
                if self.is_write_something_exist():
                    write_something = self.current_driver.find_element(By.XPATH, WRITE_SOMETHING_PATH)
                    button = self.get_clickable_button(write_something)
                    button.click()
                if self.is_text_field_in_group_exist():
                    self.write_message(message_to_post)
                    #WebDriverWait(self.current_driver, 6, 0.5).until(ec.element_to_be_clickable((By.LINK_TEXT, group)))
                    time.sleep(6)
                else:
                    print("is_text_field_in_group_is_not_exist")
                    pass  # TODO: add logger логирование в питоне
                # wait(self.current_driver, timeout=3).until(self.is_text_input_field_exist())
                # try:
                #     write_something = self.current_driver.find_element(By.XPATH, WRITE_SOMETHING_PATH)
                #     button = self.get_clickable_button(write_something)
                #     button.click()
                #     time.sleep(2)
                #     self.write_message(message_to_post)
                #     time.sleep(6)
                # except Exception as e:
                #     print(e)  # TODO: add logger логирование в питоне
                #     continue
        else:
            mb.showerror("Error", "Link to group can not be empty")
            return

    #
    # class Logger
    # def init(self, path_to_file) -> None:
    #     pass
    #
    # def log(message):
    #     pass
