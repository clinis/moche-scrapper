import os

from dotenv import load_dotenv
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

browser = Firefox()

moche_login_url = 'https://cliente.moche.pt/'
moche_area_url = 'https://cliente.moche.pt/consumos'

id_meo_username = os.getenv("ID_MEO_EMAIL")
id_meo_password = os.getenv("ID_MEO_PASSWORD")


login_page_title = 'ID MEO | Área de Cliente Moche'
login_username_field = '//*[@id="ContentPlaceHolder1_LoginTemplate_Template_WebSSOUsernameTextBox"]'
login_password_field = '//*[@id="ContentPlaceHolder1_LoginTemplate_Template_WebSSOPasswordTextBox"]'
login_btn = '//*[@id="ContentPlaceHolder1_LoginTemplate_Template_WebSSOSubmitButton"]'

data = dict()
internet = {
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
video = {
    'unit': None,
    'plafond': None,
    'available': None,
    'used': None
}

# ---

browser.get(url=moche_login_url)
browser.find_element(By.XPATH, login_username_field).send_keys(id_meo_username)
browser.find_element(By.XPATH, login_password_field).send_keys(id_meo_password)
browser.find_element(By.XPATH, login_btn).click()

browser.get(url=moche_area_url)
WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/p')))
net1 = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/p').text
net2 = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div[2]/p').text
apps1 = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[3]/div[2]/div[2]/div[2]/p').text
apps2 = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[3]/div[2]/div[2]/div[3]/div[2]/p').text
video1 = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[3]/div[2]/div[3]/div[2]/p').text
video2 = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[3]/div[2]/div[3]/div[3]/div[2]/p').text


internet['available'], internet['unit'], _ = net1.split(' ')
internet['used'], _, internet['plafond'], _ = net2.split(' ')
data['internet'] = internet

apps['available'], apps['unit'], _ = apps1.split(' ')
apps['used'], _, apps['plafond'], _ = apps2.split(' ')
data['apps'] = apps

video['available'], video['unit'], _ = video1.split(' ')
video['used'], _, video['plafond'], _ = video2.split(' ')
data['video'] = video

print(data)
