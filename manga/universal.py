# import flamescans as fs
# import luminousscans as ls
# import reaperscans as rs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
import requests
import shutil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from colorthief import ColorThief


def get_dominant_color(url_image):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_image, stream=True, headers=headers)
        with open('img.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        ct = ColorThief("img.png")
        dm_c = ct.get_palette(quality=1)
        plt.imshow([dm_c])
        dm_c = [dm_c[4][0], dm_c[4][1], dm_c[4][1]]

    except:
        return [0, 0, 0]


    #         R       G         B
    return dm_c[0], dm_c[1], dm_c[1]


def get_data(url: str):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-gpu')

    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    html = driver.page_source
    html = BeautifulSoup(html, 'html.parser')
    driver.quit()
    return html
