from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle

# 目标url
url = 'https://learn.open.com.cn/Account/Login'
browser = webdriver.Chrome()
browser.get(url)

# 等待网页渲染完成
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_element_located((By.ID, 'loginbtn')))

username = browser.find_element(By.ID, 'username')
password = browser.find_element(By.ID, 'pwd')
loginbtn = browser.find_element(By.ID, 'loginbtn')
username.send_keys('a15054854614')
password.send_keys('lqs*#06#86')

time.sleep(1)

loginbtn.click()

time.sleep(10)

# 获得成功登录后cookies
cookies = browser.get_cookies()

pickle.dump(cookies, open("cookies.pkl", "wb"))
