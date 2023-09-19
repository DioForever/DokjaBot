# REMOVED BECAUSE OF DAILY CHANGE OF URL


# import sys
# import bs4
# from universal import get_data, getLastUpdate, getNewChapters
# from universal import get_dominant_color
# import nextcord
# from database.functions import select
#
#
# # def execute(url: str):
# #     html: bs4.BeautifulSoup
# #     episodesHtml: list[str]
# #     html, episodesHtml = get_ep_list(url)
# #
# #
#
#
# def get_ep_list(url: str):
#     e: Exception = Exception(sys.exception())
#     html: bs4.BeautifulSoup = get_data(url)
#     # print(html)
#
#     episodesHtml = html.body.find('div', attrs={'id': 'chapterlist'})
#
#     episodesHtml: list[str] = (str(episodesHtml).split("data-num="))
#     try:
#         episodesHtml.pop(0)
#     except Exception as e:
#         return html, episodesHtml, e
#     return html, episodesHtml, e
#
#
# def get_thumb(html: bs4.BeautifulSoup):
#     e: Exception = Exception(sys.exception())
#
#     try:
#         thumbHtml = html.body.find('img', attrs={'class': 'attachment- size- wp-post-image'})
#         print(thumbHtml)
#         return thumbHtml, e
#     except Exception as e:
#         return "", e
#
#
# def get_title(html: bs4.BeautifulSoup):
#     e: Exception = Exception(sys.exception())
#     try:
#         titleHtml = html.body.find('h1', attrs={'class': 'entry-title'})
#         title: str = str(titleHtml).split(">")[1].split("<")[0]
#         return title, e
#     except Exception as e:
#         return "", e
#
#
# def getBookInfo(url: str):
#     e: Exception = Exception(sys.exception())
#     html, episodesHtml, eHtml = get_ep_list(url)
#     print(html)
#     print("-/-/-/-")
#     print(episodesHtml)
#     print(eHtml)
#     title, eTitle = get_title(html)
#     print(eTitle)
#     chapters, eChapters = getNewChapters(title, url)
#     for key in list(chapters.keys()):
#         print(chapters[key])
#     print(eChapters)
#     print(list(chapters.keys()))
#     print((chapters.keys())[0])
#     number = chapters[(list(chapters.keys())[0])]
#     thumb_url, eThumb = get_thumb(html)
#     print(eThumb)
#
#
# # getNewChapters("Mercenary Enrollment", "https://luminousscans.com/series/1692860401-mercenary-enrollment/")
# getBookInfo("https://luminousscans.com/series/1692860401-mercenary-enrollment/")
#              https://luminousscans.com/series/1692946801-mercenary-enrollment/
# # print(execute("https://luminousscans.com/series/1692860401-fff-class-trash-hero/"))
