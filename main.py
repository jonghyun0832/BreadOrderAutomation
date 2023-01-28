import time

import bs4
import selenium
import configparser
import datetime as dt

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

    inputBoxQueryStartDate = driver.find_element(By.ID, FRAME_ORDER_STATUS_DATE_START)
    inputBoxQueryStartDate.click()
    inputBoxQueryStartDate.send_keys("2023-01-27")

    inputBoxQueryEndDate = driver.find_element(By.ID, FRAME_ORDER_STATUS_DATE_END)
    inputBoxQueryEndDate.click()
    inputBoxQueryEndDate.send_keys("2023-01-27")

    btnFilterItem = driver.find_element(By.ID, FRAME_ORDER_STATUS_FILTER_ITEM)
    btnFilterItem.click()

    btnOrderStatusQuery = driver.find_element(By.ID, BTN_ORDER_STATUS_QUERY)
    btnOrderStatusQuery.click()


# def print_hi(name):

if __name__ == '__main__':
    # ---------------------------- Const Values ----------------------------------------------

    LOGIN_ID = config.get('LoginData', 'login_id')
    LOGIN_PASSWORD = config.get('LoginData', 'login_pw')

    FRAME_LOGIN_ID_BOX = "mainframe_FrameSet0_LoginFrame_form_div_login_div_form_edt_id_input"
    FRAME_LOGIN_PW_BOX = "mainframe_FrameSet0_LoginFrame_form_div_login_div_form_edt_pw_input"
    FRAME_LOGIN_BTN = "mainframe_FrameSet0_LoginFrame_form_div_login_div_form_btn_loginTextBoxElement"
    FRAME_MAIN_POPUP = "mainframe_FrameSet0_WorkSteFrame_POPUP_ID229"
    FRAME_MAIN_POPUP_CLOSE_BTN = "form_btn_closeTextBoxElement"
    # 주문현황 필터 - 상품별
    FRAME_ORDER_STATUS_FILTER_ITEM = "mainframe_FrameSet0_WorkSteFrame_form_div_mainWork_ORD003003_div_Contents_div_Work_div_list_tab_list_tabpage08_tabbuttonTextBoxElement"
    # 주문현황 조회기간(시작)
    FRAME_ORDER_STATUS_DATE_START = "mainframe_FrameSet0_WorkSteFrame_form_div_mainWork_ORD003003_div_Contents_div_Work_div_search_cal_fromDt_cal_dt_calendaredit_input"
    # 주문현황 조회기간(끝)
    FRAME_ORDER_STATUS_DATE_END = "mainframe_FrameSet0_WorkSteFrame_form_div_mainWork_ORD003003_div_Contents_div_Work_div_search_cal_toDt_cal_dt_calendaredit_input"

    # 주문관리 메뉴 버튼
    BTN_HOME_ORDER_MANAGEMENT = "mainframe_FrameSet0_WorkSteFrame_form_div_mainMenu_div_menuLeft_div_icon_btn_ordTextBoxElement"
    # 주문현황 메뉴 버튼
    BTN_HOME_SUB_ORDER_STATUS = "mainframe_FrameSet0_WorkSteFrame_form_div_mainMenu_div_PopMenu_grd_Menu_body_gridrow_9_cell_9_0_controltreeTextBoxElement"
    # 주문현황 조회하기 버튼
    BTN_ORDER_STATUS_QUERY = "mainframe_FrameSet0_WorkSteFrame_form_div_mainWork_ORD003003_div_WorkTop_div_Btn_btn_apprTextBoxElement"

    # ---------------------------- Main Code Starts -----------------------------------------------

    driver = webdriver.Chrome('chromedriver')
    driver.get('http://pcpos.spc.co.kr')
    driver.implicitly_wait(3)

    driver.switch_to.frame('SPC')

    print('in progress...')

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, FRAME_LOGIN_ID_BOX))
        )  # 입력창이 뜰 때까지 대기
    finally:
        pass  # TODO : 웹 페이지 로딩이 굉장히 느린 Case Handling 필요

    loginIdBox = driver.find_element(By.ID, FRAME_LOGIN_ID_BOX)
    loginIdBox.send_keys(LOGIN_ID)

    loginPassWordBox = driver.find_element(By.ID, FRAME_LOGIN_PW_BOX)
    loginPassWordBox.click()
    loginPassWordBox.send_keys(LOGIN_PASSWORD)

    loginAccessBox = driver.find_element(By.ID, FRAME_LOGIN_BTN)
    loginAccessBox.click()

    time.sleep(1)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[id^='{FRAME_MAIN_POPUP}']"))
        )  # 팝업창이 뜰 때까지 대기
    finally:
        pass  # TODO : 15초 이상 했는데 없는 경우 2가지 케이스 -> 진짜 없는경우, 로딩이 느린 경우 -> 분기 처리 필요
    time.sleep(2)

    mainPopupList = driver.find_elements(By.CSS_SELECTOR, f"[id*='{FRAME_MAIN_POPUP_CLOSE_BTN}']")
    mainPopupList.reverse()

    for popupCloseBtn in mainPopupList:
        popupCloseBtn.click()
        time.sleep(1)

    time.sleep(3)
    # 홈 화면 진입 완료

    menuOrderManagementBtn = driver.find_element(By.ID, BTN_HOME_ORDER_MANAGEMENT)
    menuOrderManagementBtn.click()
    time.sleep(1)

    menuSubOrderStatusBtn = driver.find_element(By.ID, BTN_HOME_SUB_ORDER_STATUS)
    menuSubOrderStatusBtn.click()

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[id^='{FRAME_ORDER_STATUS_FILTER_ITEM}']"))
        )  # 날짜 선택창이 뜰 때까지 대기
    finally:
        pass  # TODO : 5초 이내로 주문현황의 날짜 선택기가 로드되지 않는 경우 -> 네트워크 오류 Case로 예상 Handling 필요\

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
