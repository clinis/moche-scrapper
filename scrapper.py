import csv
import os
from datetime import datetime

from dotenv import load_dotenv
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Moche URLs
MOCHE_LOGIN_URL = 'https://cliente.moche.pt/'
MOCHE_AREA_URL = 'https://cliente.moche.pt/consumos'

# login elements
LOGIN_USERNAME_FIELD = '//*[@id="ContentPlaceHolder1_LoginTemplate_Template_WebSSOUsernameTextBox"]'
LOGIN_PASSWORD_FIELD = '//*[@id="ContentPlaceHolder1_LoginTemplate_Template_WebSSOPasswordTextBox"]'
LOGIN_BTN = '//*[@id="ContentPlaceHolder1_LoginTemplate_Template_WebSSOSubmitButton"]'

# dashboard elements
INTERNET_TEXT_1 = '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/p'
INTERNET_TEXT_2 = '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div[2]/p'
APPS_TEXT_1 = '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[3]/div[2]/div[2]/div[2]/p'
APPS_TEXT_2 = '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[3]/div[2]/div[2]/div[3]/div[2]/p'
VIDEO_TEXT_1 = '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[3]/div[2]/div[3]/div[2]/p'
VIDEO_TEXT_2 = '/html/body/div[2]/div[2]/section[1]/section[1]/section[1]/div/div[3]/div/div[3]/div[2]/div[3]/div[3]/div[2]/p'


def flatten(dict_of_dicts):
    """Flatten a dict of dicts."""

    out = {}
    for key, val in dict_of_dicts.items():
        if isinstance(val, dict):
            val = [val]
        if isinstance(val, list):
            for subdict in val:
                deeper = flatten(subdict).items()
                out.update({key + '_' + key2: val2 for key2, val2 in deeper})
        else:
            out[key] = val
    return out


def write_to_file(dict):
    """Write results to an export CSV file."""

    flatten_dict = flatten(dict)

    with open('moche_stats.csv', 'a') as export_file:
        writer = csv.DictWriter(export_file, delimiter=',', fieldnames=flatten_dict.keys())

        # if file does not exits, create and add the header
        if export_file.tell() == 0:
            writer.writeheader()

        writer.writerow(flatten_dict)


def moche_area_login(browser, credentials):
    """Login to the Moche Area website."""

    browser.get(url=MOCHE_LOGIN_URL)
    browser.find_element(By.XPATH, LOGIN_USERNAME_FIELD).send_keys(credentials.get('id_meo_username'))
    browser.find_element(By.XPATH, LOGIN_PASSWORD_FIELD).send_keys(credentials.get('id_meo_password'))
    browser.find_element(By.XPATH, LOGIN_BTN).click()


def moche_area_get_dashboard(browser):
    """Go to the Moche Area Dashboard and get the values."""

    browser.get(url=MOCHE_AREA_URL)
    WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, INTERNET_TEXT_1)))
    internet_text = [browser.find_element(By.XPATH, INTERNET_TEXT_1).text,
                     browser.find_element(By.XPATH, INTERNET_TEXT_2).text]
    apps_text = [browser.find_element(By.XPATH, APPS_TEXT_1).text, browser.find_element(By.XPATH, APPS_TEXT_2).text]
    video_text = [browser.find_element(By.XPATH, VIDEO_TEXT_1).text, browser.find_element(By.XPATH, VIDEO_TEXT_2).text]

    return internet_text, apps_text, video_text


def parse_moche_dashboard_values(internet_text, apps_text, video_text):
    """Parse values for different metrics of Moche Area."""

    internet = {'unit': None, 'plafond': None, 'available': None, 'used': None}
    apps = {'unit': None, 'plafond': None, 'available': None, 'used': None}
    video = {'unit': None, 'plafond': None, 'available': None, 'used': None}

    internet['available'], internet['unit'], _ = internet_text[0].split(' ')
    internet['used'], _, internet['plafond'], _ = internet_text[1].split(' ')

    apps['available'], apps['unit'], _ = apps_text[0].split(' ')
    apps['used'], _, apps['plafond'], _ = apps_text[1].split(' ')

    video['available'], video['unit'], _ = video_text[0].split(' ')
    video['used'], _, video['plafond'], _ = video_text[1].split(' ')

    return internet, apps, video


if __name__ == '__main__':
    load_dotenv()
    credentials = {
        'id_meo_username': os.getenv("ID_MEO_EMAIL"),
        'id_meo_password': os.getenv("ID_MEO_PASSWORD"),
    }

    fireFoxOptions = FirefoxOptions()
    fireFoxOptions.headless = True
    browser = Firefox(options=fireFoxOptions)
    moche_area_login(browser, credentials)
    internet, apps, video = parse_moche_dashboard_values(*moche_area_get_dashboard(browser))

    data = {
        'timestamp': datetime.now(),
        'internet': internet,
        'apps': apps,
        'video': video
    }
    write_to_file(data)
