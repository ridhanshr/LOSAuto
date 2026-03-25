import os
import sys

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import InvalidSessionIdException

from src.utils.db_utils import update_user
from src.utils.login_utils import perform_login
from src.utils.xlsx_utils import read_excel_data
from src.utils.assign_utils import assign_data
from src.utils.autoScoring_utils import automate_scoring
from src.utils.api_cobrand import registerCobrand, uploadDocuments, checkNoApp
from src.utils.ui_utils import setup_webdriver
from src.config import config

import time
import re
import sys
from faker import Faker


def run():
    """
    setup data
    """
    # Setup path data
    xlsxdataPath = r'Data/LOSData.xlsx'
    sheetAssignment = "Assignment"
    sheetEntryData = "Entry Data"
    sheetCard = "Card"

    # Retrieve Data
    # Branch Data
    branchData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 2)

    #Card Data
    plasticTypeData = read_excel_data(xlsxdataPath, sheetCard, 2, 4)
    limitData = read_excel_data(xlsxdataPath, sheetCard, 2, 5)
    namaProduct = read_excel_data(xlsxdataPath, sheetCard, 2, 8)

    # Assignment Data
    sendToData = read_excel_data(xlsxdataPath, sheetAssignment, 2, 1)
    sendToAppReviewer = read_excel_data(xlsxdataPath, sheetAssignment, 2, 2)

    start_time = time.time()

    # """
    # Entry Data
    # """
    # brixkeys = registerCobrand(branchData, namaProduct.upper())
    # print("brixkeys", brixkeys)

    # """
    # Upload Document
    # """
    # uploadDocuments(brixkeys,branchData)
    # noAplikasiData = checkNoApp(brixkeys)
    noAplikasiData = "KNP2025062600009"

    # """
    # Check No Aplikasi
    # """
    print("noAplikasiData", noAplikasiData)

    # """
    # Scoring
    # """
    # host = '172.24.141.33'
    # username = 'administrator'
    # password = 'c@rdl1nk'
    # pathWinSCP = r'C:/Program Files (x86)/WinSCP/WinSCP.exe'

    # time.sleep(5)
    # print("Step Scoring Mulai")

    # appFlagAfter = automate_scoring(pathWinSCP, noAplikasiData, host, username, password)

    # if appFlagAfter in ["9.2.1", "9.2.3"]:
    #     sys.exit(f"Program dihentikan karena appFlagAfter {appFlagAfter}")
    # elif appFlagAfter in ["3.5.0", "3.6.1"]:
    #     while appFlagAfter in ["3.5.0", "3.6.1"]:
    #         print("Step Scoring Diulang")
    #         appFlagAfter = automate_scoring(pathWinSCP, noAplikasiData, host, username, password)

    # print('Flag', appFlagAfter)
    # print("Proses Scoring Selesai")

    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", default=config.get("browser", "edge"), help="Browser type")
    args, unknown = parser.parse_known_args()

    # Setup webdriver based on argument or config
    fast = config.get("fast_mode", False)
    driver = setup_webdriver(args.browser, fast_mode=fast)
    driver.maximize_window()

    try:
        # Login LOS
        driver.get("http://172.24.141.61/bricc/unittest.aspx")
        print("Login")
        credentials = config.get_credentials()
        username = credentials.get("username", "cc_dam")
        perform_login(driver, username)

        """
        Credit Reviewer Assignment
        """
        update_user(noAplikasiData)
        print("Credit Reviewer Assignment Start")
        driver.get("http://172.24.141.61/bricc/ScreenMenu.aspx?sm=L|SPV&passurl&mntitle=Credit%20Reviewer%20Assignment&li1=LR|SPV|00&li2=LR|SPV|01&tc1=5.7.0&tc2=5.7.1&stg=ANLMINI")

        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))

        assign_data(driver, "mainPanel_SendTo", noAplikasiData, sendToAppReviewer)

        print("Credit Reviewer Assignment End")

        """
        Credit Reviewer
        """
        print("Credit Reviewer Start")

        # Update User
        update_user(noAplikasiData)

        # Akses Menu Credit Reviewer 
        driver.get(f"http://172.24.141.61/bricc/ScreenMenu.aspx?sm=ANLMINI&passurl&mntitle=Credit%20Reviewer&tc=5.7.1&regno={noAplikasiData}&stg=ANL")

        time.sleep(3)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Decision']"))).click()
        # access iframe
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))

        # akses elemen iframe
        limitData = read_excel_data(xlsxdataPath, sheetCard, 2, 5)
        time.sleep(5)
        # akses elemen iframe
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "mainPanel_GV_PRODUCT_cell0_6_BTN_EDIT"))).click()
        time.sleep(3)
        WebDriverWait(driver, 999).until(EC.presence_of_element_located((By.ID, 'popupDetail_panelDetail_plastictypePanel_df_PLASTICID')))
        select_element = Select(driver.find_element(By.ID, 'popupDetail_panelDetail_plastictypePanel_df_PLASTICID'))
        select_element.select_by_value(str(plasticTypeData))
        time.sleep(2)
        driver.find_element(By.ID, "popupDetail_panelDetail_df_CP_APRLIMIT").clear()
        time.sleep(1)
        driver.find_element(By.ID, "popupDetail_panelDetail_df_CP_APRLIMIT").send_keys(str(limitData))
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "popupDetail_panelDetail_Button6"))).click()
        time.sleep(10)

        WebDriverWait(driver, 620).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[4]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        WebDriverWait(driver, 620).until(EC.invisibility_of_element_located((By.ID, 'popupDetail_CSD-1')))
        time.sleep(3)

        WebDriverWait(driver, 999).until(EC.presence_of_element_located((By.ID, 'mainPanel_decPanel_dfa_AP_NEXTTRBY')))
        select_element = Select(driver.find_element(By.ID, 'mainPanel_decPanel_dfa_AP_NEXTTRBY'))
        select_element.select_by_value("DIRTONI")
        time.sleep(3)

        WebDriverWait(driver, 999).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[4]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        time.sleep(3)


        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='mainPanel_decPanel_btn_update']"))).click()
        WebDriverWait(driver, 999).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(3)
        WebDriverWait(driver, 999).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[4]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))

        # exit from iframe 
        driver.switch_to.default_content()

        print("Credit Reviewer  Step End")


        """
        Approval
        """
        print("Approval Step Start")

        # Update User
        update_user(noAplikasiData)
        print("update user berhasil")

        # akses menu approval
        driver.get(f"http://172.24.141.61/bricc/ScreenMenu.aspx?sm=APRV&passurl&mntitle=Approval&tc=7.1&regno={noAplikasiData}&stg=APRV")
        time.sleep(3)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Decision']"))).click()

        # access iframe
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))

        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.ID, "mainPanel_decPanel_btn_appr"))).click()
        WebDriverWait(driver, 999).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        WebDriverWait(driver, 999).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[4]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        time.sleep(3)

        print("Approval Step End")

        # exit from iframe 
        driver.switch_to.default_content()
        time.sleep(10)

        print("Proses Onboarding Data LOS Selesai")
        elapsed_seconds = int(time.time() - start_time)
        print(f"Proses berjalan selama : {elapsed_seconds} detik")

    finally:
        driver.quit()

if __name__ == "__main__":
    run()