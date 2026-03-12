from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from src.utils.ui_utils import save_screenshot

import logging

logger = logging.getLogger("LOSAuto.Login")

def perform_login(driver, username='cc_dam'):
    """
    Perform login operation using Selenium WebDriver.

    Parameters:
    - driver: The Selenium WebDriver instance.
    - username: The username to be entered in the login form.

    Returns:
    - None
    """
    
    actions = ActionChains(driver)
    
    # Find the text box and perform actions
    element = driver.find_element(By.ID, "TextBox1")
    actions.click(on_element=element)
    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    
    # Enter the username
    element.send_keys(username)
    
    # Take screenshot before login
    save_screenshot(driver, '1.png')

    # Click the login button
    driver.find_element(By.ID, "Button1").click()
    logger.info("Login Berhasil")
