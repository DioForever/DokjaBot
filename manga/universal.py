import sys

import bs4
import nextcord
import numpy as np
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import aiohttp
from PIL import Image
from manga.reaperscans import getBookInfoReaperScans

from database.functions import select


def gateway(url: str):
    if url.startswith("https://reaperscans.com"):
        return getBookInfoReaperScans(url)
    else:
        return None, None, None


def get_dominant_color(url: str):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        image = Image.open(response.raw)
        image = image.convert("RGB")
        img_array: np.array = np.array(image)
        average_color = np.mean(img_array, axis=(0, 1))
        dominant_color = tuple(average_color.astype(int))
        hex_color = "#{:02x}{:02x}{:02x}".format(*dominant_color)
        return hex_color

    except Exception as e:
        print("An error occurred:", e)


def get_data(url: str):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-gpu')

    # driver = webdriver.Chrome(options=chrome_options)
    chrome = ChromeDriverManager().install()
    # print(chrome)
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    html = BeautifulSoup(html, 'html.parser')
    driver.quit()
    return html


def getLastUpdate(title: str):
    value: list = select("mangaTable", "number", f"title = '{title}'")
    return value


def getNewChapters(title: str, episodesHtml):
    # print(episodesHtml)
    lastUpdate = (getLastUpdate(title))
    if lastUpdate is None: lastUpdate = 0
    # print(lastUpdate)

    episodes, e = sortUpdates(episodesHtml, lastUpdate)
    return episodes, e


def sortUpdates(episodesHtml: bs4.BeautifulSoup, lastUpdate: int):
    e: Exception = Exception(sys.exception())
    episodes = {}

    for chunk in episodesHtml:
        try:
            chunk = chunk.split('"')
            num = int(chunk[1])
            link = chunk[9]
            if num > lastUpdate:
                episodes.setdefault(link, num)
                # print(num, link)
            else:
                return episodes, e
        except Exception as e:
            return episodes, e
    return episodes, e


def createChapterEmbed(title: str, thumb: str, hexColor: str, number: float):
    embed = nextcord.Embed(title=f"{title} - Chapter {number}",
                           color=nextcord.Color.from_rgb(
                               tuple(int(hexColor.strip("#")[i:i + 2], 16) for i in (0, 2, 4))))
    try:
        embed.set_image(url=thumb)
    except Exception as e:
        return embed
    return embed


def createEmbed(title: str, description: str, thumb: str, hexColor: str):
    colors = tuple(int(hexColor.strip("#")[i:i + 2], 16) for i in (0, 2, 4))
    embed = nextcord.Embed(title=title,
                           description=description,
                           color=nextcord.Color.from_rgb(
                               colors[0], colors[1], colors[2]))
    try:
        embed.set_image(url=thumb)
    except Exception as e:
        return embed
    return embed
