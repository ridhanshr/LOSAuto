from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def select_dropdown_by_value(driver, element_id, value):
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, element_id)))
    select_element = Select(driver.find_element(By.ID, element_id))
    select_element.select_by_value(str(value))