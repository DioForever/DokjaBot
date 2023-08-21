import bs4
from universal import get_data
from universal import get_dominant_color
import nextcord


def execute(url: str):
    html, episodesHtml = get_ep_list(url)
    # print(html, episodesHtml)

    if True:
        r, g, b = (get_dominant_color(url))
        embed = nextcord.Embed(title=f"Required Administrator perms!",
                               color=nextcord.Color.from_rgb(r, g, b))


def check_if_new():
    pass


def get_ep_list(url: str):
    html = get_data(url)
    # print(html)

    episodesHtml = html.body.find('div', attrs={'id': 'chapterlist'})
    print("---")

    episodesHtml = (str(episodesHtml).split("data-num="))
    print(f"Episodes html {episodesHtml}")
    print(f"Episode html {episodesHtml[1]}")
    try:
        episodesHtml.remove(0)
    except:
        return html, episodesHtml
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


execute("https://luminousscans.com/series/1692601201-fff-class-trash-hero/")
