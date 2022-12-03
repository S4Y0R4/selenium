import collections
import time
from selenium.common.exceptions import NoSuchElementException
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

ANOTHER_PEOPLE_BUTTON_PATH = "/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div/div[" \
                             "1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/span/div/div/div" \
                             "[1]/div/div/div[1]/i"

LOADING_POST_PL = "//span[text()='Publikowanie']"

ABSOLUTE_CHROME_PATH = r"C:\Users\r1kk4\PycharmProjects\selenium\selenium\chrome\chromedriver.exe"

BLOCK_WARNING = "//span[text()='powiadom nas o tym']"

CAN_NOT_POSTING_ALERT = "/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[3]/div/div[1]/div"


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
            executable_path=ABSOLUTE_CHROME_PATH,
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
        # self.is_driver_online = False
        # self.current_driver.quit()

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
        self.gui.status_switch_auth_btn()
        self.gui.status_switch_stop_posting_btn()

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

    def is_can_not_posting_alert_exist(self):
        try:
            WebDriverWait(self.current_driver, 1, 0.25).until(
                ec.visibility_of_element_located((By.XPATH, CAN_NOT_POSTING_ALERT)))
            logger.log("WARNING BAN IS COMING")
            return True
        except TimeoutException:
            return False

    def is_home_button_exist(self) -> bool:
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, HOME_BUTTON_PATH)))
            logger.log("HOME_BUTTON was found")
            return True
        except TimeoutException:
            logger.log("ERROR" + ": " + "HOME_BUTTON was not found")
            return False

    def is_picture_button_exist(self) -> bool:
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, PICTURE_BUTTON_PATH)))
            logger.log("PICTURE_BUTTON was found")
            return True
        except TimeoutException:
            logger.log("ERROR" + ": " + "PICTURE_BUTTON was not found")
            return False

    def is_cookie_button_exist(self) -> bool:
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, COOKIE_BUTTON_PATH)))
            logger.log("COOKIE_BUTTON was found")
            return True
        except TimeoutException:
            logger.log("ERROR" + ": " + "COOKIE_BUTTON was not found")
            return False

    def is_text_field_in_group_exist(self) -> bool:
        if self.is_people_button_exist() or self.is_another_people_button_exist():
            logger.log("TEXT FIELD IS EXIST")
            return True
        else:
            logger.log("ERROR" + ": " + "TEXT FIELD IS NOT EXIST")
            return False

    def is_people_button_exist(self) -> bool:
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, PEOPLE_BUTTON_PATH)))
            logger.log("ERROR" + ": " + "PEOPLE_BUTTON was found")
            return True
        except TimeoutException:
            logger.log("ERROR" + ": " + "PEOPLE_BUTTON was not found")
            return False

    def is_another_people_button_exist(self) -> bool:
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, ANOTHER_PEOPLE_BUTTON_PATH)))
            logger.log("ANOTHER_PEOPLE_BUTTON was found")
            return True
        except TimeoutException:
            logger.log("ERROR" + ": " + "ANOTHER_PEOPLE_BUTTON was not found")
            return False

    def home_page(self):
        self.current_driver.get("https://facebook.com")

    @staticmethod
    def is_file_path_not_empty(file_path) -> bool:
        return len(file_path) > 0

    def is_links_not_empty(self) -> bool:
        return len(self.links) > 0

    def set_groups_from_file(self, file_path: str):
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

    @staticmethod
    def is_message_not_empty(message: str) -> bool:
        if len(message) == 0:
            return False

    def write_message(self, message: str):
        if self.is_message_not_empty:
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

    def is_write_something_exist(self) -> bool:
        try:
            WebDriverWait(self.current_driver, 2, 0.3).until(
                ec.visibility_of_element_located((By.XPATH, WRITE_SOMETHING_PATH)))
            logger.log("ERROR" + ": " + "WRITE_SOMETHING_PATH was found")
            return True
        except TimeoutException:
            logger.log("ERROR" + ": " + "WRITE_SOMETHING_PATH was not found")
            return False

    def start_posting(self, message_to_post):
        if self.is_links_not_empty():
            self.is_posting = True
            logger.log("posting button status was changed to normal")
            self.gui.status_switch_posting_btn()
            self.gui.status_switch_stop_posting_btn()
            self.gui.status_switch_open_btn()
            self.gui.handle_posting_started()
            for group in self.links:
                if self.is_posting:
                    self.current_driver.get(group)
                    # self.gui.handle_link_changed(group)#TODO: HANDLE LINK
                    if self.is_write_something_exist():
                        write_something = self.current_driver.find_element(By.XPATH, WRITE_SOMETHING_PATH)
                        button = self.get_clickable_button(write_something)
                        button.click()
                    if self.is_text_field_in_group_exist():
                        self.write_message(message_to_post)
                        if self.is_can_not_posting_alert_exist() or self.is_block_warning_exist():
                            self.home_page()
                            self.is_posting = False
                            self.gui.status_switch_posting_btn()
                            self.gui.status_switch_stop_posting_btn()
                            self.gui.status_switch_open_btn()
                            logger.log(
                                "WARNING" + ": " + "A blocking warning has been received, it is recommended that you \
                                end your account")
                        else:
                            self.is_loading_post_pl_disappeared()
                    else:
                        logger.log("ERROR" + ": " + "text field in group is not exist")
                        continue
            self.home_page()
            self.is_posting = False
            self.gui.status_switch_posting_btn()
            self.gui.status_switch_stop_posting_btn()
            self.gui.status_switch_open_btn()
            # self.gui.status_switch_auth_btn()
            logger.log("Posting is over. Now you can choose another .txt file")
            return mb.showinfo("Posting is over", "Now you can choose another .txt file")
        else:
            logger.log("ERROR" + ": " + "Link to group can not be empty")
            return mb.showerror("Error", "Link to group can not be empty")

    def is_loading_post_pl_disappeared(self):
        while True:
            try:
                self.current_driver.find_element(By.XPATH, LOADING_POST_PL)
            except NoSuchElementException:
                break

    def is_block_warning_exist(self):
        try:
            self.current_driver.find_element(By.XPATH, BLOCK_WARNING)
        except NoSuchElementException:
            logger.log("BLOCK WARNING!!!")
            mb.showwarning("BLOCK WARNING!",
                           """The account has been temporarily suspended, please restart the program as a different\
                            user. To avoid this, please use the program wisely!""")


class Logger:

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def log(self, message):
        with open(self.path_to_file, "a") as log_file:
            log_file.write(message + "\n")
            log_file.close()


logger = Logger(r"C:\Users\r1kk4\OneDrive\Рабочий стол\logs.txt")
