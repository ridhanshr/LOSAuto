import os
import sys

# Add project root to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from openpyxl import load_workbook
from src.utils.db_utils import update_appflag, update_user, update_norek, check_appflag, update_accnum
from src.utils.login_utils import perform_login
from src.utils.xlsx_utils import read_excel_data, count_filled_rows
from src.utils.docCheck_utils import update_document
from src.utils.dataEntry_utils import select_dropdown_by_value
from src.utils.assign_utils import assign_data
from src.utils.ui_utils import setup_webdriver, save_screenshot
from src.utils.autoScoring_utils import automate_scoring
from src.config import config

import time
import re
import sys
import random
import os
from faker import Faker

from src.utils.logging_utils import setup_logging
import logging

def main():
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", default=config.get("browser", "edge"), help="Browser type")
    parser.add_argument("--log-level", default=config.get("log_level", "info"), help="Log level")
    parser.add_argument("--fast", action="store_true", help="Run in fast/headless mode")
    args, unknown = parser.parse_known_args()

    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger("LOSAuto.Recontest")

    # Fast mode: reduced delays
    fast = args.fast
    def wait(seconds):
        """Adaptive sleep: reduced in fast mode."""
        time.sleep(max(0.5, seconds * 0.3) if fast else seconds)

    driver = setup_webdriver(args.browser, fast_mode=args.fast)

    try:
        # Setup path data
        xlsxdataPath = config.get("data_file", "Data/LOSData.xlsx")
        sheetEntryData = "Entry Data"
        sheetDocCheck = "Document Checking"
        sheetJobInfo = "Job Info"
        sheetAssignment = "Assignment"
        sheetEmergency = "Emergency Contact"
        sheetOtherOptions = "Other Options"
        sheetCard = "Card"

        # Retrieve Data
        fake = Faker('en_NZ')
        qrCodeData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 1)
        branchData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 2)
        channelData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 3)
        kodeProgramData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 4)
        jenisNasabahData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 5)
        salesIDData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 6)
        namaNasabahData = fake.name_male()
        namaPanggilanData = namaNasabahData
        namaCetakArr = namaNasabahData.split(' ')
        namaCetakData = namaCetakArr[0]
        jenisKelaminData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 10)
        tempatLahirData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 12)
        tanggalLahirData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 13)
        bulanLahirData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 14)
        tahunLahirData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 15)
        eKTPData = str(random.randint(10**15, 10**16 - 1))
        statusPernikahanData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 17)
        jumlahTanggunganData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 18)
        pendidikanData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 19)
        namaIbuData = fake.name_female()
        identitasPajakData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 21)
        alamatRumahData1 = read_excel_data(xlsxdataPath, sheetEntryData, 2, 22)
        alamatRumahData2 = read_excel_data(xlsxdataPath, sheetEntryData, 2, 23)
        alamatRumahData3 = read_excel_data(xlsxdataPath, sheetEntryData, 2, 24)
        alamatRT = read_excel_data(xlsxdataPath, sheetEntryData, 2, 25)
        alamatRW = read_excel_data(xlsxdataPath, sheetEntryData, 2, 26)
        alamatLurah = read_excel_data(xlsxdataPath, sheetEntryData, 2, 27) 
        alamatCamat = read_excel_data(xlsxdataPath, sheetEntryData, 2, 28) 
        kotaData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 29)
        kodePosData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 30)
        telpRumahPrefixData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 31)
        telpRumahData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 32)
        telpHPData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 33)
        statusRumahData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 34)
        lamaMenempatiThnData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 35)
        lamaMenempatiBlnData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 36)
        NPWPData = str(random.randint(10**14, 10**15 - 1))
        emailData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 38)
        noAplikasiData = read_excel_data(xlsxdataPath, sheetEntryData, 2, 39)

        workbook = load_workbook(xlsxdataPath)
        sheet1 = workbook['Entry Data']
        sheet1.cell(row=2, column=7).value = namaNasabahData
        sheet1.cell(row=2, column=8).value = namaPanggilanData
        sheet1.cell(row=2, column=9).value = namaCetakData
        sheet1.cell(row=2, column=16).value = eKTPData
        sheet1.cell(row=2, column=20).value = namaIbuData
        sheet1.cell(row=2, column=37).value = NPWPData
        workbook.save(xlsxdataPath)

        # Document Check Data
        docCheckData1 = read_excel_data(xlsxdataPath, sheetDocCheck, 2, 1)
        docCheckData3 = read_excel_data(xlsxdataPath, sheetDocCheck, 4, 1)
        docCheckData4 = read_excel_data(xlsxdataPath, sheetDocCheck, 5, 1)
        docCheckData6 = read_excel_data(xlsxdataPath, sheetDocCheck, 7, 1)
        docCheckData7 = read_excel_data(xlsxdataPath, sheetDocCheck, 8, 1)

        # Job Info Data
        # ... (rest of data retrieval)
        bidangUsahaData = read_excel_data(xlsxdataPath, sheetJobInfo, 2, 3)
        lamaBekerjaThnData = read_excel_data(xlsxdataPath, sheetJobInfo, 2, 4)
        lamaBekerjaBlnData = read_excel_data(xlsxdataPath, sheetJobInfo, 2, 5)
        pendapatanData = read_excel_data(xlsxdataPath, sheetJobInfo, 2, 7)

        # Emergency Contact Data
        hubunganEmergency = read_excel_data(xlsxdataPath, sheetEmergency, 2, 2)
        alamatEmergency = read_excel_data(xlsxdataPath, sheetEmergency, 2, 3)
        kotaEmergency = read_excel_data(xlsxdataPath, sheetEmergency, 2, 4)

        #Other Options Data
        pilihanBSData = read_excel_data(xlsxdataPath, sheetOtherOptions, 2, 3)
        noRekData = read_excel_data(xlsxdataPath, sheetOtherOptions, 2, 4)

        #Card Data
        plasticTypeData = read_excel_data(xlsxdataPath, sheetCard, 2, 4)
        limitData = read_excel_data(xlsxdataPath, sheetCard, 2, 5)

        # Assignment Data
        sendToData = read_excel_data(xlsxdataPath, sheetAssignment, 2, 1)
        sendToAppReviewer = read_excel_data(xlsxdataPath, sheetAssignment, 2, 2)

        start_time = time.time()
        """
        login
        """
        driver.get("http://172.24.141.61/bricc/unittest.aspx")
        logger.info("Login")
        perform_login(driver)

        """
        generate QR
        """
        wait(2)
        logger.info("Generate QR Step Start")
        driver.get("http://172.24.141.61/bricc/ScreenMenu.aspx?sm=BAR|G&passurl&mntitle=Generate%20Barcode&row=8&barfontsize=40&barsize=100&imgwidth=250&borderwidth=0&altalign=1&padtop=20&rowheight=73&colwidth=350&cellspacing=0")
        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        driver.find_element(By.XPATH, "//input[@id='mainPanel_branchPanel_BRANCHID_txtID']").send_keys('99010')
        driver.find_element(By.XPATH, "//input[@id='mainPanel_btn_gen']").click()
        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        image_element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='mainPanel_tbl']/tbody/tr[2]/td[1]/img")))
        image_url = image_element.get_attribute('src')
        qrCode = image_url.split("data=")[1].split("&")[0]
        workbook = load_workbook(xlsxdataPath)
        sheet1 = workbook['Entry Data']
        sheet1.cell(row=2, column=1).value = qrCode
        workbook.save(xlsxdataPath)
        driver.switch_to.default_content()
        logger.info("Generate QR Step End")

        """
        Initial Data Entry
        """
        logger.info("Initial Data Entry Step Start")
        driver.get("http://172.24.141.61/bricc/ScreenMenu.aspx?sm=IDE|C&passurl&mntitle=Re-Contest&tc=1.0&stg=DE&reap=CON")
        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.ID, "mainPanel_Button1"))).click()
        wait(1)
        driver.find_element(By.ID, "PopFindBasic_PNL_FindBasic_fAP_REGNO").send_keys(noAplikasiData)
        wait(2)
        WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.XPATH, "(//input[@value='Find'])[1]"))).click()
        WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.ID, "PopFindBasic_PNL_FindBasic_GridViewX_cell0_7_Button4"))).click()
        wait(3)
        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        driver.find_element(By.XPATH, "(//input[@id='mainPanel_df_BARCODE'])[1]").send_keys('9901000000007')
        wait(3)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mainPanel_eventPanel_df_EVENTID")))
        Select(driver.find_element(By.ID, "mainPanel_eventPanel_df_EVENTID")).select_by_value(str(9999999995))
        WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.ID, f"mainPanel_df_PLASTICID_{plasticTypeData}"))).click()
        wait(1)
        WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.ID, "mainPanel_Button2"))).click()
        wait(3)
        for _ in range(2):
            try:
                WebDriverWait(driver, 50).until(EC.alert_is_present())
                driver.switch_to.alert.accept()
                wait(5)
            except:
                pass
        WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[1]/td[2]')))
        driver.switch_to.default_content()
        logger.info('Initial Data Entry Step End')

        """
        Document Checking
        """
        logger.info("Document Checking Step Start")
        wait(2)
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        elementNoAplikasi = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "UC_GeneralInfo1_l1")))
        valueNoAplikasi = elementNoAplikasi.text
        wait(2)
        workbook = load_workbook(xlsxdataPath)
        sheet1 = workbook['Entry Data']
        sheet1.cell(row=2, column=39).value = valueNoAplikasi
        workbook.save(xlsxdataPath)
        docCheckDataList = [docCheckData1, docCheckData3, docCheckData4, docCheckData6, docCheckData7]
        for docCheckData in docCheckDataList:
            WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.ID, "griddoc_header7_Button4"))).click()
            WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
            update_document(driver, docCheckData)
            WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
            wait(3)
        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        wait(3)
        WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.ID, "updPanel_btnUpdate"))).click()
        for _ in range(2):
            try:
                WebDriverWait(driver, 30).until(EC.alert_is_present())
                driver.switch_to.alert.accept()
                wait(2)
            except:
                pass
        driver.switch_to.default_content()
        logger.info("Document Checking Step End")

        """
        Data Entry Assignment
        """
        logger.info("Data Entry Assignment Step Start")
        driver.get("http://172.24.141.61/bricc/ScreenMenu.aspx?sm=L|SPV|DE&passurl&mntitle=Data%20Entry%20Assignment&li1=LR|A|SPV|DE|00&li2=LR|A|SPV|DE|01&tc1=3.0&tc2=3.1&atype=DE&stg=DE&xlcode=DE")
        WebDriverWait(driver, 320).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        assign_data(driver, "mainPanel_sendtoPanel_SendTo", valueNoAplikasi, sendToData)
        logger.info("Data Entry Assignment Step End")

        """
        Data Entry
        """
        logger.info("Data Entry Step Start")
        driver.get(f"http://172.24.141.61/bricc/ScreenMenu.aspx?sm=DE&passurl&mntitle=Data%20Entry&tc=3.1&regno={valueNoAplikasi}&stg=DE")
        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Personal Info']"))).click()
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='mainPanel_CU_NICKNM']")))
        driver.find_element(By.XPATH, "//input[@id='mainPanel_CU_NMCARD']").send_keys(namaCetakData)
        driver.find_element(By.XPATH, "//input[@id='mainPanel_CU_BORNPLACE']").send_keys(tempatLahirData)
        driver.find_element(By.ID, "mainPanel_CU_EMAIL").send_keys(emailData)
        Select(driver.find_element(By.ID, "mainPanel_CU_ED_CODE")).select_by_value(str(pendidikanData))
        Select(driver.find_element(By.ID, "mainPanel_CU_TAXIDFLAG")).select_by_value(str(identitasPajakData))
        driver.find_element(By.XPATH, "//input[@id='mainPanel_CU_MMNMFIRST']").send_keys(namaIbuData)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "mainPanel_BTN_SAVE"))).click()
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        wait(3)
        WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[1]/td[2]')))
        driver.switch_to.default_content()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Job Info']"))).click()
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.ID, "mainPanel_CU_COMPNAME")))
        wait(1)
        driver.find_element(By.XPATH, "//select[@id='mainPanel_CU_OFCTCODE']").send_keys("PT")
        driver.find_element(By.ID, "mainPanel_CU_BUSSINESSDESC").send_keys(bidangUsahaData)
        driver.find_element(By.XPATH, "//select[@id='mainPanel_CU_TOTEMP_CODE']").send_keys("4")
        wait(1)
        driver.find_element(By.ID, "mainPanel_CU_WORKSINCEYY").clear()
        driver.find_element(By.ID, "mainPanel_CU_WORKSINCEYY").send_keys(lamaBekerjaThnData)
        driver.find_element(By.ID, "mainPanel_CU_WORKSINCEMM").clear()
        driver.find_element(By.ID, "mainPanel_CU_WORKSINCEMM").send_keys(lamaBekerjaBlnData)
        driver.find_element(By.ID, "mainPanel_CU_INCOME").send_keys(pendapatanData)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.ID, "mainPanel_BTN_SAVE"))).click()
        WebDriverWait(driver, 999).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Emergency Contact']"))).click()
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        Select(driver.find_element(By.ID, "mainPanel_CU_EMRE_CODE")).select_by_value(str(hubunganEmergency))
        driver.find_element(By.ID, "mainPanel_CU_EMHMADDR1").send_keys(alamatEmergency)
        driver.find_element(By.ID, "mainPanel_CU_EMHMCITY").send_keys(kotaEmergency)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "mainPanel_BTN_SAVE"))).click()
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        wait(3)
        WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[1]/td[2]')))
        driver.switch_to.default_content()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Other Options']"))).click()
        update_accnum(valueNoAplikasi)
        wait(1)
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        Select(driver.find_element(By.ID, "mainPanel_BILLING_STAT_TYPE")).select_by_value(str(pilihanBSData))
        driver.find_element(By.ID, "mainPanel_AD_ACCNUM").send_keys('0')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "mainPanel_BTN_SAVE"))).click()
        wait(3)
        WebDriverWait(driver, 50).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        wait(3)
        WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[1]/td[2]')))
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Main']"))).click()
        wait(3)
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        WebDriverWait(driver, 620).until(EC.element_to_be_clickable((By.ID, "mainPanel_btn_update"))).click()
        for _ in range(2):
            try:
                WebDriverWait(driver, 30).until(EC.alert_is_present())
                driver.switch_to.alert.accept()
                wait(3)
            except:
                pass
        driver.switch_to.default_content()
        logger.info("Data Entry Step End")

        """
        DE Validation Assignment
        """
        logger.info("DE Validation Assignment Step Start")
        driver.get("http://172.24.141.61/bricc/ScreenMenu.aspx?sm=L|SPV&passurl&mntitle=DE%20Validation%20Assignment&li1=LR|SPV|DE|00&li2=LR|SPV|01&tc1=3.5.0&tc2=3.5.1&stg=VDE")
        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        assign_data(driver, "mainPanel_SendTo", valueNoAplikasi, sendToData)
        logger.info("DE Validation Assignment Step End")

        """
        DE Validation
        """
        wait(3)
        logger.info("Data Entry Validation Step Start")
        update_user(valueNoAplikasi)
        driver.get(f"http://172.24.141.61/bricc/ScreenMenu.aspx?sm=VDE&passurl&mntitle=Data%20Entry%20Validation&tc=3.5.1&regno={valueNoAplikasi}&stg=DE")
        wait(3)
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.ID, "mainPanel_btn_update"))).click()
        for _ in range(2):
            try:
                WebDriverWait(driver, 50).until(EC.alert_is_present())
                driver.switch_to.alert.accept()
                wait(5)
            except:
                pass
        driver.switch_to.default_content()
        logger.info("Data Entry Validation Step End")

        """
        Scoring
        """
        host = '172.24.141.33'
        usernameScoring = 'administrator'
        passwordScoring = 'c@rdl1nk'
        pathWinSCP = r'C:/Program Files (x86)/WinSCP/WinSCP.exe'
        logger.info("Proses Scoring Mulai")
        appFlagAfter = automate_scoring(pathWinSCP, valueNoAplikasi, host, usernameScoring, passwordScoring)
        if appFlagAfter in ["9.2.1", "9.2.3"]:
            sys.exit(f"Program dihentikan karena appFlagAfter {appFlagAfter}")
        logger.info("Proses Scoring Selesai")

        """
        Credit Reviewer Assignment
        """
        logger.info("Credit Reviewer Assignment Start")
        wait(3)
        driver.get("http://172.24.141.61/bricc/ScreenMenu.aspx?sm=L|SPV&passurl&mntitle=Credit%20Reviewer%20Assignment&li1=LR|SPV|00&li2=LR|SPV|01&tc1=5.7.0&tc2=5.7.1&stg=ANLMINI")
        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[2]/td[1]/table[2]/tbody[1]/tr[1]/td[2]/span[1]')))
        assign_data(driver, "mainPanel_SendTo", valueNoAplikasi, sendToAppReviewer)
        logger.info("Credit Reviewer Assignment End")

        """
        Credit Reviewer
        """
        logger.info("Credit Reviewer Start")
        update_user(valueNoAplikasi)
        wait(3)
        driver.get(f"http://172.24.141.61/bricc/ScreenMenu.aspx?sm=ANLMINI&passurl&mntitle=Credit%20Reviewer&tc=5.7.1&regno={valueNoAplikasi}&stg=ANL")
        wait(10)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Decision']"))).click()
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        wait(5)
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "mainPanel_GV_PRODUCT_cell0_6_BTN_EDIT"))).click()
        wait(3)
        driver.find_element(By.ID, "popupDetail_panelDetail_df_CP_APRLIMIT").send_keys(str(limitData))
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "popupDetail_panelDetail_Button6"))).click()
        wait(10)
        WebDriverWait(driver, 620).until(EC.invisibility_of_element_located((By.ID, 'popupDetail_CSD-1')))
        Select(driver.find_element(By.ID, 'mainPanel_decPanel_dfa_AP_NEXTTRBY')).select_by_value("DIRTONI")
        wait(3)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='mainPanel_decPanel_btn_update']"))).click()
        WebDriverWait(driver, 999).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()
        logger.info("Credit Reviewer Step End")
        
        # Login again for approval as different user
        driver.get("http://172.24.141.61/bricc/unittest.aspx")
        perform_login(driver, username='tsipsd')

        """
        Approval
        """
        logger.info("Approval Step Start")
        update_user(valueNoAplikasi, ap_nexttrby='tsipsd')
        driver.get(f"http://172.24.141.61/bricc/ScreenMenu.aspx?sm=APRV&passurl&mntitle=Approval&tc=7.1&regno={valueNoAplikasi}&stg=APRV")
        wait(10)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Decision']"))).click()
        WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.ID, "mainPanel_decPanel_btn_appr"))).click()
        WebDriverWait(driver, 999).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()
        wait(10)

        if (noRekData != 0):
            update_norek(str(valueNoAplikasi), str(noRekData))

        logger.info("Proses Onboarding Data LOS Selesai")
        logger.info(f"Time: {int(time.time() - start_time)}s")

    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()