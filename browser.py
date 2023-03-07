from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle

driver = None


def init_browser(url):
    global driver
    # 初始化 Chrome 浏览器
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 使用 headless 模式，即不显示浏览器窗口
    driver = webdriver.Chrome(options=options)

    driver.get('https://learn.open.com.cn')

    # 将 cookie 添加到浏览器中
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    # 打开网页
    driver.get(url)

    # 等待网页渲染完成
    wait_for_element_by_class_name('groupItemId')


def wait_for_element_by_class_name(class_name):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))


# 获取当前 tab Dom
def get_current_tab(key):
    currentTab = None
    items = driver.find_elements(By.CLASS_NAME, 'groupItemId ')
    for _, item in enumerate(items):
        if key == item.text:
            currentTab = item
            break
    return currentTab


def get_navigation_label_num_list():
    ul = driver.find_element(By.CLASS_NAME, 'm-pagination-page')
    li = ul.find_elements(By.TAG_NAME, 'li')
    hasNextPageBtn = any(item.text == '下一页' for item in li)
    if hasNextPageBtn:
        return list(range(0, len(li) - 1))
    else:
        return list(range(0, len(li)))


# 获取导航标签
def get_navigation_label(index):
    ul = driver.find_element(By.CLASS_NAME, 'm-pagination-page')
    aList = ul.find_elements(By.TAG_NAME, 'a')
    name = str(index + 1)
    for a in aList:
        if a.text == name:
            return a
    return None


# 获取当前页数据
def get_page_data():
    titles = list(
        map(lambda x: x.text,
            driver.find_elements(By.CLASS_NAME, "Subject-Title")))

    # 判断是否有选项
    noOptions = len(driver.find_elements(By.CLASS_NAME, "right-answer")) == 0

    if noOptions:
        answers = list(
            map(lambda x: x.text,
                driver.find_elements(By.CLASS_NAME, "fill-back-cont")))
    else:
        answers = list(
            map(lambda x: x.text,
                driver.find_elements(By.CLASS_NAME, "right-answer")))

    return titles, answers


def get_tabs():
    return list(
        map(lambda item: item.text,
            driver.find_elements(By.CLASS_NAME, 'groupItemId ')))


def get_data():
    subject_title = []
    right_answer = []

    # 标签页
    tabs = get_tabs()

    for _, tab in enumerate(tabs):
        print(tab, 'tab')
        currentTab = get_current_tab(tab)
        currentTab.click()
        wait_for_element_by_class_name('Subject-Title')

        pageNoList = get_navigation_label_num_list()
        for index in pageNoList:
            if index == 0:
                wait_for_element_by_class_name('Subject-Title')
                titles, answers = get_page_data()
                subject_title.extend(titles)
                right_answer.extend(answers)
                continue
            a = get_navigation_label(index)
            if a is None:
                continue
            a.click()
            wait_for_element_by_class_name('Subject-Title')
            titles, answers = get_page_data()
            subject_title.extend(titles)
            right_answer.extend(answers)

    return subject_title, right_answer


def quit_browser():
    driver.quit()
