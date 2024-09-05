from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def update_document(driver, docCheckData):
    WebDriverWait(driver, 320).until(EC.presence_of_element_located((By.ID, "Popupdoc_Paneldoc_DOC_CODE")))
    time.sleep(3)
    select = Select(driver.find_element(By.ID, "Popupdoc_Paneldoc_DOC_CODE"))
    select.select_by_value(str(docCheckData))
    time.sleep(1)

    WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='Popupdoc_Paneldoc_DOC_AVAIL']"))).click()
    WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='Popupdoc_Paneldoc_DOC_VALID']"))).click()
    WebDriverWait(driver, 320).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='Popupdoc_Paneldoc_btn_update']"))).click()

    WebDriverWait(driver, 620).until(EC.invisibility_of_element_located((By.ID, 'Popupdoc_CSD-1')))
    time.sleep(1)

    print(f"Update Document {docCheckData} berhasil")
