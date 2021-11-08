import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class BaseCrawler(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    def get(self, url):
        self.browser.get(url)

    def find_by_id(self, identifier):
        return self.browser.find_element(By.ID, identifier)

    def find_by_class(self, class_name):
        return self.browser.find_element(By.CLASS_NAME, class_name)

    #def get_by_class(self, class_name):
     #   return self.browser.get_(By.CLASS_NAME(class_name))

    def find_elements_by_css_selector(self, css_selector):
        return self.browser.find_element(By.CSS_SELECTOR, css_selector)

    def find_elements_by_class_name(self, class_name):
        return self.browser.find_elements(By.CLASS_NAME, class_name)

    def find_element_by_class_name(self, class_name):
        return self.browser.find_element(By.CLASS_NAME, class_name)

    def find_element_by_xpath(self, xpath):
        return self.browser.find_element(By.XPATH, xpath)

    def find_elements_by_xpath(self, xpath):
        return self.browser.find_elements(By.XPATH, xpath)

    def scroll_bottom(self, steps=1, sleep=1):
        try:
            for _ in range(steps):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(sleep)
        except Exception as ex:
            print(ex)
            print("Error haciendo scroll")

    def scroll_until_end(self):
        scroll_pause_time = 0.5
        last_height = None

        while True:
            # Scroll down to bottom
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.execute_script("return document.body.scrollHeight")

            if last_height is not None and new_height == last_height:
                break

            last_height = new_height

    def run(self):
        raise NotImplementedError()

    def execute_script(self, param):
        return self.execute_script(param)
