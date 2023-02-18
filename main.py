import re
import time

import bs4
import selenium
import configparser
import datetime as dt
import constants.HtmlConstants as HTML
import constants.CsvConstants as CSV
import pandas as pd
import os
import numpy as np

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

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[id^='{HTML.FRAME_MAIN_POPUP}']"))
        )  # 팝업창이 뜰 때까지 대기
    finally:
        pass  # TODO : 15초 이상 했는데 없는 경우 2가지 케이스 -> 진짜 없는경우, 로딩이 느린 경우 -> 분기 처리 필요


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

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[id^='{HTML.FRAME_ORDER_STATUS_FILTER_ITEM}']"))
        )  # 날짜 선택창이 뜰 때까지 대기
    finally:
        pass  # TODO : 5초 이내로 주문현황의 날짜 선택기가 로드되지 않는 경우 -> 네트워크 오류 Case로 예상 Handling 필요


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

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[id^='{HTML.ITEM_RESULT_ROW_FIRST}']"))
        )  # 쿼리 결과가 나올때까지 대기
    finally:
        pass  # TODO : 5초 이내로 선택한 날짜 조회가 안될 경우 -> 네트워크 오류 Case로 예상 Handling 필요


def get_item_csv():
    btnExportCSV = driver.find_element(By.ID, HTML.BTN_ORDER_STATUS_EXPORT_CSV)
    btnExportCSV.click()


def get_index_from_csv(target):
    productRowList, productColumnList = np.where(csv == target)
    productHeaderRow = productRowList[0]
    productColumnRow = productColumnList[0]
    return productHeaderRow, productColumnRow


if __name__ == '__main__':
    # ---------------------------- Get Local Properties Values ----------------------------------------------
    #
    LOGIN_ID = config.get('LoginData', 'login_id')
    LOGIN_PASSWORD = config.get('LoginData', 'login_pw')
    #
    # # ---------------------------- Main Code Starts -----------------------------------------------
    #
    driver = webdriver.Chrome('chromedriver')
    driver.get('http://pcpos.spc.co.kr')
    driver.implicitly_wait(3)
    #
    # driver.switch_to.frame('SPC')
    #
    # try:
    #     element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.ID, HTML.FRAME_LOGIN_ID_BOX))
    #     )  # 입력창이 뜰 때까지 대기
    # finally:
    #     pass  # TODO : 웹 페이지 로딩이 굉장히 느린 Case Handling 필요
    #
    # # 메인 화면 로그인
    # login_to_home()
    #
    # # 팝업 리스트 제거
    # close_pop_up_list()
    # time.sleep(1)
    #
    # # 주문 현황으로 이동
    # go_to_order_status()
    #
    # # 조회할 날짜 가져오기 (현재 날짜 기준)
    # queryDate = get_query_date()
    # # 주문현황 입력 날짜로 조회하기 (현재 하루만 조회하기 때문에 같은 날짜 입력)
    # order_status_query(queryDate, queryDate)
    #
    # # 엑셀로 가져오기
    # get_item_csv()
    #
    # time.sleep(8)
    #
    # # TODO : 함수로 바꾸기
    # # 다운받은 엑셀 파일 데이터 읽어오기

    userAbsolutePath = os.path.expanduser('~')
    downloadPath = userAbsolutePath + "/Downloads"
    print(downloadPath)

    csvPath = downloadPath + "/"

    # os.chdir(downloadPath)
    testList = os.listdir(downloadPath)

    # # TODO : 예외처리, excel 파일이 없을 경우,
    for test in testList:
        if test.endswith("_주문현황.xlsx"):
            csvPath = csvPath + test
            break

    #CSV 파일 읽고, 필요한 데이터 스크랩핑
    csv = pd.read_excel(csvPath)
    productHeaderRow, productHeaderColumn = get_index_from_csv(CSV.PRODUCT_NAME)
    productTotalRow, productTotalColumn = get_index_from_csv(CSV.PRODUCT_TOTAL)

    for i in range(productHeaderRow + 2, productTotalRow):
        productCode = csv.iloc[i, 6]
        productName = csv.iloc[i, 7]
        orderNum = csv.iloc[i, 16]
        print(f"{productCode:>10} {orderNum:10}개 \t {productName:<20} ")



    # page_source = driver.page_source
    #
    # soup = BeautifulSoup(page_source, 'html.parser')
    #
    # body = soup.find('div', attrs={"id": "mainframe_FrameSet0_WorkSteFrame_form_div_mainWork_ORD003003_div_Contents_div_Work_div_list_grd_ordItemList_body_gridrow_0"})
    #
    # # 테스트중-----------------------------------------
    # # test_ids = soup.find_all("mainframe_FrameSet0_WorkSteFrame_form_div_mainWork_ORD003003_div_Contents_div_Work_div_list_grd_ordItemList_body_gridrow")  # id 속성이 "test_id"인 모든 요소를 리스트형태로 반환
    #
    # test_ids = soup.select('#mainframe_FrameSet0_WorkSteFrame_form_div_mainWork_ORD003003_div_Contents_div_Work_div_list_grd_ordItemList_body_gridrow_0_cell_0_6GridCellTextContainerElement > div')
    #
    # # test2 = soup.select_one("#mainframe_FrameSet0_WorkSteFrame_form_div_mainWork_ORD003003_div_Contents_div_Work_div_list_grd_ordItemList_body_gridrow_0_cell_0_6GridCellTextContainerElement > div").string
    # print(f'body : {body}\n test_ids : {test_ids}')
    #
    # divs1 = soup.find_all("div", {"id": re.compile('^6GridCellTextContainerElement')})
    # divs2 = soup.find_all("div", {"id": re.compile('6GridCellTextContainerElement$')})

    # for div in divs2 :

    # print(f'div1 : {divs1}\n div2 : {divs2.__len__()}')
