import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from . import config,tags
import  threading

ENV=config.get_env()
class Session():
    '''get session of requests with cookies'''
    _lock=threading.Lock()
    def __init__(self):
        self.headers=ENV.get(tags.HEADERS)
        option = Options()
        option.add_argument("--headless")
        option.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=option)
        self.sessions={}
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not hasattr(Session,'_instance'):
                cls._instance=object.__new__(cls)
        return cls._instance
    def login(self):
        pass
    # @property
    def get_session(self):
        html_source = self.driver.page_source
        cookies = self.driver.get_cookies()
        sess = requests.session()
        sess.headers.update(self.headers)
        for cookie in cookies:
            sess.cookies.set(cookie["name"], cookie["value"])
        try:
            csrf = re.search("window.csrf = '(.*?)'", html_source).group(1)
            sess.headers.update({"csrf": csrf})
        except AttributeError:
            pass
        return sess
    def close(self):
        self.driver.close()

class HdProdSession(Session):
    # def __int__(self):
    #     super().__init__()
    def _login(self,url):
        name=ENV.get(tags.LOGIN_NAME)
        password=ENV.get(tags.PASSWORD)
        login_type=ENV.get((tags.LOGIN_TYPE))
        self.driver.get(url)
        if int(login_type) == 1:
            self.driver.find_element_by_id("name").send_keys(name)
            self.driver.find_element_by_id("pwd1").send_keys(password)
            self.driver.find_element_by_xpath(r'//a[@onclick="login()"]').click()
        elif int(login_type) == 2:
            self.driver.find_element_by_id("username").send_keys(name)
            self.driver.find_element_by_id("pwd1").send_keys(password)
            self.driver.find_element_by_css_selector(r'input[value="立即登录"]').click()
        time.sleep(1)
        # wait = WebDriverWait(self.driver, 10)
        # wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/script")))
        return self.driver
    def get_session(self,module=None):
        '在sessions字典中找到对应的session，没有则添加'
        if module:
            if module not in self.sessions.keys():
                url = ENV.get('{}_url'.format(module))
                self._login(url)
                self.driver.get(url)
                sess=super(HdProdSession,self).get_session()
                self.close()
                self.sessions[module]=sess
            return self.sessions[module]