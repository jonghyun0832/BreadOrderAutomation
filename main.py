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
        pass

    loginIdBox = driver.find_element(By.ID, FRAME_LOGIN_ID_BOX)
    loginIdBox.send_keys(LOGIN_ID)

    loginPassWordBox = driver.find_element(By.ID, FRAME_LOGIN_PW_BOX)
    loginPassWordBox.click()
    loginPassWordBox.send_keys(LOGIN_PASSWORD)

    loginAccessBox = driver.find_element(By.ID, FRAME_LOGIN_BTN)
    loginAccessBox.click()

    time.sleep(1)

    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[id^='{FRAME_MAIN_POPUP}']"))
        )  # 입력창이 뜰 때까지 대기
    finally:
        pass

    time.sleep(2)

    mainPopupList = driver.find_elements(By.CSS_SELECTOR, f"[id*='{FRAME_MAIN_POPUP_CLOSE_BTN}']")
    mainPopupList.reverse()

    for popupCloseBtn in mainPopupList:
        popupCloseBtn.click()
        time.sleep(1)

    time.sleep(3)

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
