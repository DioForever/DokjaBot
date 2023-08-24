import sys

import bs4
from universal import get_data
from universal import get_dominant_color
import nextcord
from database.functions import select


def execute(url: str):
    html: bs4.BeautifulSoup
    episodesHtml: list[str]
    html, episodesHtml = get_ep_list(url)


def getNewChapters(title: str, episodesHtml: str):
    e: Exception = Exception(sys.exception())

    print(episodesHtml)
    episodes = {}
    lastUpdate = (getLastUpdate(title))
    print(lastUpdate)
    for chunk in episodesHtml:
        try:
            chunk = chunk.split('"')
            num = int(chunk[1])
            link = chunk[9]
            if num > lastUpdate:
                episodes.setdefault(link, num)
                print(num, link)
            else:
                return episodes, e
        except Exception as e:
            return episodes, e

    return episodes, e


def getLastUpdate(title: str):
    value = select("mangaTable", "number", f"title = '{title}'")
    return value


def get_ep_list(url: str):
    html = get_data(url)
    # print(html)

    episodesHtml = html.body.find('div', attrs={'id': 'chapterlist'})
    print("---")

    episodesHtml: list[str] = (str(episodesHtml).split("data-num="))
    try:
        episodesHtml.pop(0)
    except Exception as e:
        return html, episodesHtml, e
    return html, episodesHtml
    # print(type(html))


def get_thumb(embed: nextcord.Embed, html: bs4.BeautifulSoup):
    try:
        url = html.body.find('div', attrs={'class': 'thumb'})
        url = url.body.find('img')
        url = url['src']
        embed.set_image(url=str(url))
        return embed
    except:
        return embed


def get_title():
    pass


print(execute("https://luminousscans.com/series/1692860401-fff-class-trash-hero/"))
