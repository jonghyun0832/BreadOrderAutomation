import time

import bs4
import selenium
import configparser


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
    FRAME_ORDER_STATUS_FILTER_ITEM = "mainframe_FrameSet0_WorkSteFrame_form_div_mainWork_ORD003003_div_Contents_div_Work_div_list_tab_list_tabpage08_tabbuttonTextBoxElement"
    FRAME_ORDER_STATUS_DATE_START = "mainframe_FrameSet0_WorkSteFrame_form_div_mainWork_ORD003003_div_Contents_div_Work_div_search_cal_fromDt_cal_dt_calendaredit_input"

    # 주문관리
    BTN_HOME_ORDER_MANAGEMENT = "mainframe_FrameSet0_WorkSteFrame_form_div_mainMenu_div_menuLeft_div_icon_btn_ordTextBoxElement"
    # 주문현황
    BTN_HOME_SUB_ORDER_STATUS = "mainframe_FrameSet0_WorkSteFrame_form_div_mainMenu_div_PopMenu_grd_Menu_body_gridrow_9_cell_9_0_controltreeTextBoxElement"

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
        pass # TODO : 웹 페이지 로딩이 굉장히 느린 Case Handling 필요

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
        pass # TODO : 15초 이상 했는데 없는 경우 2가지 케이스 -> 진짜 없는경우, 로딩이 느린 경우 -> 분기 처리 필요
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

    menuSubOrderStatusBtn = driver.find_element(By.ID,  BTN_HOME_SUB_ORDER_STATUS)
    menuSubOrderStatusBtn.click()

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[id^='{FRAME_ORDER_STATUS_FILTER_ITEM}']"))
        )  # 날짜 선택창이 뜰 때까지 대기
    finally:
        pass # TODO : 5초 이내로 주문현황의 날짜 선택기가 로드되지 않는 경우 -> 네트워크 오류 Case로 예상 Handling 필요

    print("Load Complete")

    inputBoxQueryStartDate = driver.find_element(By.ID, FRAME_ORDER_STATUS_DATE_START)
    inputBoxQueryStartDate.click()
    inputBoxQueryStartDate.send_keys("2023-01-27")

    time.sleep(5)

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
