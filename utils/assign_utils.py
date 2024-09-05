from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

def assign_data(driver, elementSendto, noAplikasiData, sendToData):
    # Access iframe
    WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))

    # Access element in iframe
    WebDriverWait(driver, 320).until(EC.visibility_of_element_located((By.ID, "mainPanel_grid_DXFREditorcol0_I"))).send_keys(noAplikasiData)
    driver.switch_to.default_content()
    WebDriverWait(driver, 999).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'framex')))
    WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, '//body[1]/form[1]/div[3]/div[1]/table[2]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/table[4]/tbody[1]/tr[1]/td[1]')))
    time.sleep(10)
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "mainPanel_grid_DXSelBtn0_D"))).click()
    WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.ID, elementSendto)))    
    select = Select(driver.find_element(By.ID, elementSendto))
    select.select_by_value(str(sendToData)) 

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainPanel']/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[5]/td/input[1]"))).click()
    WebDriverWait(driver, 50).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print(alert.text)
    alert.accept()
    time.sleep(3)

    WebDriverWait(driver, 320).until(EC.invisibility_of_element((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[1]/td[2]')))

    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Confirm']"))).click()
    WebDriverWait(driver, 50).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print(alert.text)
    alert.accept()
    time.sleep(1)

    WebDriverWait(driver, 320).until(EC.invisibility_of_element_located((By.XPATH, '//body[1]/form[1]/div[3]/table[2]/tbody[1]/tr[1]/td[2]')))
    time.sleep(1)
    
    # Exit from iframe 
    driver.switch_to.default_content()