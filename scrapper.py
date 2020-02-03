import os

from dotenv import load_dotenv
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

load_dotenv()

browser = Firefox()

login_url = 'https://cliente.moche.pt/'
login_username = os.getenv("MOCHEEMAIL")
login_password = os.getenv("MOCHEPASSWORD")

title_login_page = 'ID MEO | Área de Cliente Moche'

browser.get(url=login_url)
login_username_field = browser.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_LoginTemplate_Template_WebSSOUsernameTextBox"]')
login_username_field.send_keys(login_username)
login_password_field = browser.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_LoginTemplate_Template_WebSSOPasswordTextBox"]')
login_password_field.send_keys(login_password)
login_btn = browser.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_LoginTemplate_Template_WebSSOSubmitButton"]')
login_btn.click()

see_more_btn = browser.find_element(By.XPATH, '//*[@id="1bf95d9d-3e2c-4107-a900-7cfc95c83e57"]/div/a')
see_more_btn.click()

data = dict()
internet = {
    'unit': None,
    'plafond': None,
    'available': None,
    'used': None
}
sms = {
    'unit': None,
    'plafond': None,
    'available': None,
    'used': None
}
apps = {
    'unit': None,
    'plafond': None,
    'available': None,
    'used': None
}


browser.implicitly_wait(10)
data['net'] = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/p').text
data['sms'] = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[2]/div[1]/div[1]/div/div/span').text
data['apps'] = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[3]/div[2]/div[2]/div[2]/p').text
data['voz'] = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[4]/div[2]/div[2]/div[2]/p').text

print(data)
