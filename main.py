import time

import bs4
import selenium
import configparser
import datetime as dt
import constants.HtmlConstants as HTML

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

config = configparser.RawConfigParser()
config.read('local.properties')


def login_to_home():
    loginIdBox = driver.find_element(By.ID, HTML.FRAME_LOGIN_ID_BOX)
    loginIdBox.send_keys(LOGIN_ID)

    loginPassWordBox = driver.find_element(By.ID, HTML.FRAME_LOGIN_PW_BOX)
    loginPassWordBox.click()
    loginPassWordBox.send_keys(LOGIN_PASSWORD)

    loginAccessBox = driver.find_element(By.ID, HTML.FRAME_LOGIN_BTN)
    loginAccessBox.click()


def close_pop_up_list():
    mainPopupList = driver.find_elements(By.CSS_SELECTOR, f"[id*='{HTML.FRAME_MAIN_POPUP_CLOSE_BTN}']")
    mainPopupList.reverse()

    for popupCloseBtn in mainPopupList:
        popupCloseBtn.click()
        time.sleep(1)


def go_to_order_status():
    menuOrderManagementBtn = driver.find_element(By.ID, HTML.BTN_HOME_ORDER_MANAGEMENT)
    menuOrderManagementBtn.click()

    menuSubOrderStatusBtn = driver.find_element(By.ID, HTML.BTN_HOME_SUB_ORDER_STATUS)
    menuSubOrderStatusBtn.click()


# return : 어제 날짜 String Format (0000-00-00)
def get_query_date() -> str:
    datetimeNow = dt.date.today()
    datetimeYesterday = datetimeNow - dt.timedelta(1)
    convertedStrYesterday = datetimeYesterday.strftime("%Y-%m-%d")
    return convertedStrYesterday


# input(start_date) : 조회 시작 날짜
# input(end_date) : 조회 끝 날짜
def order_status_query(start_date: str, end_date: str):
    print("Order Status Query Start")

    inputBoxQueryStartDate = driver.find_element(By.ID, HTML.FRAME_ORDER_STATUS_DATE_START)
    inputBoxQueryStartDate.click()
    inputBoxQueryStartDate.send_keys(start_date)

    inputBoxQueryEndDate = driver.find_element(By.ID, HTML.FRAME_ORDER_STATUS_DATE_END)
    inputBoxQueryEndDate.click()
    inputBoxQueryEndDate.send_keys(end_date)

    btnFilterItem = driver.find_element(By.ID, HTML.FRAME_ORDER_STATUS_FILTER_ITEM)
    btnFilterItem.click()

    btnOrderStatusQuery = driver.find_element(By.ID, HTML.BTN_ORDER_STATUS_QUERY)
    btnOrderStatusQuery.click()


if __name__ == '__main__':
    # ---------------------------- Get Local Properties Values ----------------------------------------------

    LOGIN_ID = config.get('LoginData', 'login_id')
    LOGIN_PASSWORD = config.get('LoginData', 'login_pw')

    # ---------------------------- Main Code Starts -----------------------------------------------

    driver = webdriver.Chrome('chromedriver')
    driver.get('http://pcpos.spc.co.kr')
    driver.implicitly_wait(3)

    driver.switch_to.frame('SPC')

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, HTML.FRAME_LOGIN_ID_BOX))
        )  # 입력창이 뜰 때까지 대기
    finally:
        pass  # TODO : 웹 페이지 로딩이 굉장히 느린 Case Handling 필요

    # 메인 화면 로그인
    login_to_home()

    time.sleep(1)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[id^='{HTML.FRAME_MAIN_POPUP}']"))
        )  # 팝업창이 뜰 때까지 대기
    finally:
        pass  # TODO : 15초 이상 했는데 없는 경우 2가지 케이스 -> 진짜 없는경우, 로딩이 느린 경우 -> 분기 처리 필요

    # 팝업 리스트 제거
    close_pop_up_list()

    time.sleep(1)

    # 주문 현황으로 이동
    go_to_order_status()

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[id^='{HTML.FRAME_ORDER_STATUS_FILTER_ITEM}']"))
        )  # 날짜 선택창이 뜰 때까지 대기
    finally:
        pass  # TODO : 5초 이내로 주문현황의 날짜 선택기가 로드되지 않는 경우 -> 네트워크 오류 Case로 예상 Handling 필요

    # 조회할 날짜 가져오기 (현재 날짜 기준)
    queryDate = get_query_date()
    # 주문현황 입력 날짜로 조회하기 (현재 하루만 조회하기 때문에 같은 날짜 입력)
    order_status_query(queryDate, queryDate)

    time.sleep(10)

    # page_source = driver.page_source
    #
    # soup = BeautifulSoup(page_source, 'html.parser')
    #
    # body = soup.find('body')  # body 태그 요소
    #
    # spans = soup.find_all('span')  # 모든 span 요소를 리스트[]형태로 반환
    #
    # test_ids = soup.find_all("test_id")  # id 속성이 "test_id"인 모든 요소를 리스트형태로 반환
    #
    # print(f'body : {body}\n spans : {spans}\n test_ids : {test_ids}')
    # print('done')
