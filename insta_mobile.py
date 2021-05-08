import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class InstaMobile():

    def __init__(self, new=False):
        super().__init__()

        options = Options()
        if not new:
            options.add_argument(
                "user-data-dir=C:\\Users\\musta\\AppData\\Local\\Google\\Chrome\\User Data")
        options.add_argument(
            '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')

        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(230, 550)

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
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".aOOlW.HoLwm"))).click()
        except Exception as e:
            print("Could not skip: ", e)

    def watch_stories(self):
        driver = self.driver
        self.driver.get("https://instagram.com")
        time.sleep(4)
        stories = driver.find_elements_by_class_name("OE3OK")

        try:
            if int(stories[0].find_element_by_class_name("CfWVH").get_attribute("height")) < 66:
                return
        except:
            print("noo")
        stories[0].click()

        try:
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".aOOlW.HoLwm"))).click()
        except:
            print("no notification box")
        while True:
            time.sleep(1)
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_4sLyX"))).click()

            except Exception as e:
                print("no")
                print(e)
                break

    def explore(self):
        self.driver.get("https://www.instagram.com/explore/")
        time.sleep(5)
        posts = [post.get_attribute('href') for post in self.driver.find_elements_by_css_selector(
            ".QzzMF.Igw0E.IwRSH.eGOV_._4EzTm.NUiEW > a")]
        for i, post in enumerate(posts):
            self.like_post(post)
            print(f"Like posts: {i} out of {len(posts)}")
            input()

    def like_post(self, post_url=None):
        try:
            if post_url:
                self.driver.get(post_url)
            button = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "fr66n"))).find_element_by_class_name("wpO6b")
            # create action chain object
            action = ActionChains(self.driver)
            # perform the operation
            action.move_to_element(button).perform()
            button.click()
        except Exception as e:
            print("no liky")
            print(e)

    def follow_post(self, post_url=None):
        try:
            if post_url:
                self.driver.get(post_url)
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "bY2yH")))\
                .find_element_by_css_selector(".sqdOP.yWX7d.y3zKF").click()

        except Exception as e:
            print("no liky")
            print(e)

    def get_follower_list(self, count):
        
        users = set()

        # step 3
        actionChain = webdriver.ActionChains(self.driver)

        for i in range(1, count):
            try:
                username = self.driver.find_element_by_xpath(
                    f"/html/body/div[1]/section/main/div/ul/div/li[{i}]/div/div[1]/div[2]/div[1]/a").text
                users.add(username)
                print(f"{username} --> {len(users)} out of {count}")
            except:
                break

        return users

    def find_not_followers(self, user_url):

        self.driver.get(user_url)

        time.sleep(3)

        counts = self.driver.find_elements_by_class_name("g47SY")

        counts[1], counts[2] = int(counts[1].text.replace(
            ".", "")), int(counts[2].text.replace(".", ""))

        users_arr = []
        for i in range(1, 3):
            self.driver.find_elements_by_class_name("_81NM2")[i].click()
            time.sleep(2)

            users = self.get_follower_list(counts[i])
            users_arr.append(users)
            self.driver.get(user_url)
            time.sleep(2)
            # self.driver.find_elements_by_class_name("QBdPU")[1].click()

        print(users_arr[1] - users_arr[0])


ig = InstaMobile(new=True)

ig.login("cataltasz", "mus123")
ig.skip_save_password()
ig.skip_notifications()
ig.watch_stories()
# ig.find_not_followers("https://www.instagram.com/cataltasz/")
# ig.explore()
