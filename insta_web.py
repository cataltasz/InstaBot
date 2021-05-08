import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


class InstaWeb:

    def __init__(self, new=False):
        options = Options()

        if not new:
            options.add_argument(
                "user-data-dir=C:\\Users\\musta\\AppData\\Local\\Google\\Chrome\\User Data")
        self.driver = webdriver.Chrome(options=options)

    def login(self, username, password):
        driver = self.driver
        driver.get(
            "https://www.instagram.com/accounts/login/?source=auth_switcher")

        time.sleep(1)

        if self.driver.current_url != "https://www.instagram.com/":
            user_name_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username")))

            # user_name_elem = driver.find_element_by_name("username")
            user_name_elem.clear()
            user_name_elem.send_keys(username)

            pass_elem = driver.find_element_by_name("password")
            pass_elem.clear()
            pass_elem.send_keys(password)
            pass_elem.send_keys(Keys.RETURN)
            time.sleep(3)

    def skip_save_password(self):
        try:
            if self.driver.current_url == r"https://www.instagram.com/accounts/onetap/?next=%2F":
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cmbtv"))).click()
            else:
                print("lala")
            return True
        except Exception as e:
            print("Could not skip: ", e)
            return False

    def skip_notifications(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "s4Iyt")))
            self.driver.find_element_by_class_name(
                "mt3GC").find_element_by_css_selector(".aOOlW.HoLwm").click()
        except Exception as e:
            print("Could not skip: ", e)

    def go_to_home(self):
        if self.driver.current_url != "https://www.instagram.com/":
            self.driver.get("https://www.instagram.com/")
            time.sleep(2)

        return self.driver.current_url == "https://www.instagram.com/"

    def watch_stories(self):
        driver = self.driver

        if not self.go_to_home():
            print("Only stories at home page! ")
            raise Exception()

        stories = driver.find_elements_by_class_name("OE3OK")
        stories[0].click()
        while True:
            time.sleep(1)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "coreSpriteRightChevron"))).click()

            except Exception as e:
                print("no")
                print(e)
                break

    def like_posts(self):

        posts = self.driver.find_elements_by_class_name("fr66n")
        # posts = self.driver.find_elements_by_class_name("QBdPU")
        print(len(posts))

        for post in posts:
            # self.driver.execute_script("arguments[0].scrollIntoView();", post)
            post.find_element_by_class_name("QBdPU").click()
            input()

    def explore(self):
        self.driver.get("https://www.instagram.com/explore/")
        time.sleep(5)
        posts = self.driver.find_elements_by_class_name(
            "pKKVh")

        for post in posts:
            post.click()
            self.like_explore_post()
            # time.sleep(2)

    def like_explore_post(self):
        try:
            time.sleep(1)
            button = self.driver.find_element_by_class_name(
                "fr66n").find_element_by_class_name("wpO6b")
            # create action chain object
            action = ActionChains(self.driver)

            # perform the operation
            action.move_to_element(button).click().perform()
            if "Takip Et" in self.driver.page_source:
                self.driver.find_element_by_class_name("bY2yH").find_element_by_css_selector(
                    ".sqdOP.yWX7d.y3zKF").click()
                input()

        except Exception as e:
            print("no liky")
            print(e)
        self.driver.find_elements_by_class_name(
            "QBdPU")[-1].click()

    def collect_likes(self, post_url, opened=False):
        if not opened:
            self.driver.get(post_url)
            time.sleep(3)

        limit = int(self.driver.find_element_by_css_selector(
            "#react-root > section > main > div > div.ltEKP > article > div.eo2As > section.EDfFK.ygqzn > div > div > button > span").text.replace(".", ""))
        self.driver.find_element_by_class_name(
            "Nm9Fw").find_element_by_css_selector(".sqdOP.yWX7d._8A5w5").click()
        time.sleep(1)
        # Get Dialog
        xxx = self.driver.find_element_by_xpath(
            '//div[@role="dialog"]/div[1]/div[2]/div[1]/div[1]')
        # Focus on and Scroll
        xxx.click()
        # step 3
        actionChain = webdriver.ActionChains(self.driver)

        last_len = -1
        users = set()

        while(len(users) < limit-1):
            for i in range(1, 1000):
                try:
                    users.add(self.driver.find_element_by_xpath(
                        '//div[@role="dialog"]/div[1]/div[2]/div[1]/div[1]/div[' + str(i) + ']/div[2]/div[1]/div[1]').text)
                except:
                    break
            if last_len == len(users):
                break
            last_len = len(users)
            print(f"{len(users)} out of {limit}")
            xxx.click()
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(0.5)
        print(users)
        print(len(users))

        return users
