from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.wildfireaware.co.uk")

WebDriverWait(driver, 10)
inputElement = driver.find_element_by_id("searchText")
inputElement.send_keys('susanville')

inputElement.send_keys(Keys.ENTER)

driver.get_screenshot_as_file('test.png') 