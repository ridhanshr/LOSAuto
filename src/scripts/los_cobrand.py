from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

from src.utils.logging_utils import setup_logging
import logging

def run():
    # Setup path data
    xlsxdataPath = config.get("data_file", "Data/LOSData.xlsx")
    sheetAssignment = "Assignment"
    sheetEntryData = "Entry Data"
    sheetCard = "Card"

    # Retrieve Data
    branchData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 2)
    plasticTypeData = read_excel_data(xlsxdataPath, sheetCard, 2, 4)
    limitData = read_excel_data(xlsxdataPath, sheetCard, 2, 5)
    namaProduct = read_excel_data(xlsxdataPath, sheetCard, 2, 8)
    sendToData = read_excel_data(xlsxdataPath, sheetAssignment, 2, 1)
    sendToAppReviewer = read_excel_data(xlsxdataPath, sheetAssignment, 2, 2)

    brixkeys = registerCobrand(branchData, namaProduct.upper())
    uploadDocuments(brixkeys,branchData)
    noAplikasiData = checkNoApp(brixkeys)

    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", default=config.get("browser", "edge"), help="Browser type")
    parser.add_argument("--log-level", default=config.get("log_level", "info"), help="Log level")
    parser.add_argument("--fast", action="store_true", help="Run in fast/headless mode")
    args, unknown = parser.parse_known_args()

    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger("LOSAuto.Cobrand")

    driver = setup_webdriver(args.browser, fast_mode=args.fast)

    try:
        start_time = time.time()

        # ========== SCORING ==========
        hostScoring = '172.24.141.33'
        usernameScoring = 'administrator'
        passwordScoring = 'c@rdl1nk'
        pathWinSCP = r'C:/Program Files (x86)/WinSCP/WinSCP.exe'

        logger.info("Step Scoring Mulai")
        appFlagAfter = automate_scoring(pathWinSCP, noAplikasiData, hostScoring, usernameScoring, passwordScoring)

        if appFlagAfter in ["9.2.1", "9.2.3"]:
            sys.exit(f"Program dihentikan karena appFlagAfter {appFlagAfter}")
        elif appFlagAfter in ["3.5.0", "3.6.1"]:
            while appFlagAfter in ["3.5.0", "3.6.1"]:
                logger.info("Step Scoring Diulang")
                appFlagAfter = automate_scoring(pathWinSCP, noAplikasiData, hostScoring, usernameScoring, passwordScoring)

        logger.info(f'Flag {appFlagAfter}')
        logger.info("Proses Scoring Selesai")

        # Login LOS
        driver.get("http://172.24.141.61/bricc/unittest.aspx")
        logger.info("Login")
        perform_login(driver)

        # ========== CREDIT REVIEWER ASSIGNMENT ==========
        update_user(noAplikasiData)
        logger.info("Credit Reviewer Assignment Start")
        driver.get("http://172.24.141.61/bricc/ScreenMenu.aspx?sm=L|SPV&passurl&mntitle=Credit%20Reviewer%20Assignment&li1=LR|SPV|00&li2=LR|SPV|01&tc1=5.7.0&tc2=5.7.1&stg=ANLMINI")
        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        assign_data(driver, "mainPanel_SendTo", noAplikasiData, sendToAppReviewer)
        logger.info("Credit Reviewer Assignment End")

        # ========== CREDIT REVIEWER ==========
        logger.info("Credit Reviewer Step Start")
        update_user(noAplikasiData)
        driver.get(f"http://172.24.141.61/bricc/ScreenMenu.aspx?sm=ANLMINI&passurl&mntitle=Credit%20Reviewer&tc=5.7.1&regno={noAplikasiData}&stg=ANL")
        time.sleep(3)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Decision']"))).click()
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        time.sleep(5)
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "mainPanel_GV_PRODUCT_cell0_6_BTN_EDIT"))).click()
        time.sleep(3)
        WebDriverWait(driver, 999).until(EC.presence_of_element_located((By.ID, 'popupDetail_panelDetail_plastictypePanel_df_PLASTICID')))
        Select(driver.find_element(By.ID, 'popupDetail_panelDetail_plastictypePanel_df_PLASTICID')).select_by_value(str(plasticTypeData))
        time.sleep(2)
        driver.find_element(By.ID, "popupDetail_panelDetail_df_CP_APRLIMIT").clear()
        time.sleep(1)
        driver.find_element(By.ID, "popupDetail_panelDetail_df_CP_APRLIMIT").send_keys(str(limitData))
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "popupDetail_panelDetail_Button6"))).click()
        time.sleep(10)
        WebDriverWait(driver, 620).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[4]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        WebDriverWait(driver, 620).until(EC.invisibility_of_element_located((By.ID, 'popupDetail_CSD-1')))
        time.sleep(3)
        Select(driver.find_element(By.ID, 'mainPanel_decPanel_dfa_AP_NEXTTRBY')).select_by_value("DIRTONI")
        time.sleep(3)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='mainPanel_decPanel_btn_update']"))).click()
        WebDriverWait(driver, 999).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()
        logger.info("Credit Reviewer Step End")

        # ========== APPROVAL ==========
        logger.info("Approval Step Start")
        update_user(noAplikasiData)
        driver.get(f"http://172.24.141.61/bricc/ScreenMenu.aspx?sm=APRV&passurl&mntitle=Approval&tc=7.1&regno={noAplikasiData}&stg=APRV")
        time.sleep(3)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Decision']"))).click()
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.ID, "mainPanel_decPanel_btn_appr"))).click()
        WebDriverWait(driver, 999).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()
        logger.info("Approval Step End")

        logger.info("Proses Onboarding Data LOS Selesai")
        logger.info(f"Time: {int(time.time() - start_time)}s")

    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    run()