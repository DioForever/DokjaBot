from universal import get_data
from bs4 import BeautifulSoup
import nextcord

html = get_data("https://flamescans.org/series/1688551321-is-this-hero-for-real/")
print(html)
html = BeautifulSoup(html, 'html.parser')
episodesHtml = html.body.find('div', attrs={'id': 'chapterlist'})
print("---")
print(str(episodesHtml).split("data-num"))


def getThumb(embed: nextcord.Embed):

    try:
        embed.set_image()
        return embed
    except:
        return embed
