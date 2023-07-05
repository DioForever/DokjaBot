# import flamescans as fs
# import luminousscans as ls
# import reaperscans as rs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_data(url: str):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html
