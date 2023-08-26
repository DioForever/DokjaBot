import sys

import bs4

import manga.universal as universal


def getBookInfoReaperScans(url: str):
    html: bs4.BeautifulSoup = universal.get_data(url)
    print(html)
    thumb, eThumb = get_thumb(html)
    title, eTitle = get_title(html)
    episodes, eEpisodes = get_ep_list(html, title)
    print(episodes)
    if (eThumb or eTitle or eEpisodes) is None:
        return None
    return episodes, title, thumb


def get_ep_list(html: bs4.BeautifulSoup, title: str):
    e: Exception = Exception(sys.exception())

    episodesHtmlBS: bs4.BeautifulSoup = html.body.find('ul', attrs={'role': 'list'})
    episodesHtmlLS: list[bs4.BeautifulSoup] = episodesHtmlBS.find_all('li')
    episodes = {}
    latestNumber = universal.getLastUpdate(title)
    if latestNumber is None:
        latestNumber: float = 0
    latestNumber: float = float(latestNumber)
    for ep in episodesHtmlLS:
        number = float(
            f"{(ep.find('p', attrs={'class': 'truncate font-medium text-neutral-200'})).get_text()}".split(" ")[1])
        url = f"{(ep.find('a', attrs={'class': 'block transition hover:bg-neutral-800'}))['href']}"
        if (number is not None and url is not None) and number > latestNumber:
            episodes.setdefault(number, url)

    return episodes, e


def get_thumb(html: bs4.BeautifulSoup):
    e: Exception = Exception(sys.exception())
    try:
        thumbHtml: bs4.BeautifulSoup = html.body.find('img', attrs={'class': 'h-full w-full lg:h-full lg:w-full'})
        thumb = thumbHtml['src']
        print(thumb)
        return thumb, e
    except Exception as e:
        return "", e


def get_title(html: bs4.BeautifulSoup):
    e: Exception = Exception(sys.exception())
    try:
        titleHtml: bs4.BeautifulSoup = html.body.find('h1', attrs={
            'class': 'focus:outline-none font-semibold text-xl text-neutral-700 dark:text-white lg:mt-0 truncate'})
        title = titleHtml.get_text()
        print(title)
        return title, e
    except Exception as e:
        return "", e

# getBookInfo("https://reaperscans.com/comics/5150-sss-class-suicide-hunter")
