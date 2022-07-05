import discord
import requests as req
from bs4 import BeautifulSoup as bs
import callables as call
from PIL import Image

headers = {
    'User-Agent': 'Mozilla/5.0'}


# Reaper Scans
def getReaperScans(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay, id_guild):
    web = req.get(url=urlbasic, headers=headers)
    chapter_number = 0
    soup = bs(web.content, features="html.parser")
    chapter = soup.find("li", class_="wp-manga-chapter")
    thumbnail_text = str(chapter.find("img", class_="thumb"))
    thumbnail_text = thumbnail_text.split('"')
    url_thumbnail = thumbnail_text[len(thumbnail_text) - 2]
    # Now I have the thumbnail

    # Now I need the chapter number
    chapter_text = str(chapter.find("p", class_="chapter-manhwa-title")).split()
    chapter_number = float(str(chapter_text[2]).split('<')[0])

    # Now I have the number as well

    embed = call.doCheck(id_guild, Title, chapter_number, rHour, rMin, rDay, urlbasic, urlchapter, url_thumbnail, r1, g,
                         b)

    return embed, chapter_number


def getReaperScansReleased(Title, urlbasic, urlchapter, r1, g, b, id_channel, id_guild):
    web = req.get(url=urlbasic, headers=headers)
    chapter_number = float(0)
    soup = bs(web.content, features="html.parser")
    chapter = soup.find("li", class_="wp-manga-chapter")
    thumbnail_text = str(chapter.find("img", class_="thumb"))
    thumbnail_text = thumbnail_text.split('"')
    url_thumbnail = thumbnail_text[len(thumbnail_text) - 2]
    # Now I need the chapter number
    chapter_text = str(chapter.find("p", class_="chapter-manhwa-title")).split()
    chapter_number = float(str(chapter_text[2]).split('<')[0])
    chapter_number_text = chapter_number
    if str(chapter_number).split('.')[0] != '0':
        chapter_number_text = str(chapter_number).split('.')[0] + '-' + str(chapter_number).split('.')[1]

    urlchapter += f'{chapter_number_text}/'

    releaseR = call.doReleased(id_guild, Title, chapter_number, urlbasic, urlchapter, r1, g, b, url_thumbnail)
    released = releaseR[0]
    embed = releaseR[1]
    subscription = releaseR[2]

    return released, embed, subscription, chapter_number


def searchReaperScans(Title):
    title = str(Title).lower().replace(" ", "-").replace("’", "")
    url = f"https://reaperscans.com/series/{title}/"
    web = req.get(url, headers=headers)
    soup = bs(web.content, features="html.parser")
    title = ""
    urlbasic = ""
    urlchapter = ""
    # I am looking for a div with class post-title
    if soup.find("div", class_="post-title") is not None:
        # I checked if there is a 404 not found picture, so if there isnt, it was found
        found = True
        urlbasic = url
        urlchapter = f"{urlbasic}chapter-"
        print("Found")
    else:
        found = False
        print("Not Found")
    # print(soup)
    print(url)
    # I will find the title now,
    try:
        title = str(soup.find("div", class_="post-title")).split(">")[4].split("<")[0].replace("\n", "").replace("\t",
                                                                                                                 "")
    except:
        title = "Title Not Found"
    print(title)
    # I will need to get RGB of the thumb
    # so first I get the thumbnail
    try:
        url_thumb = str(soup.find("div", class_="summary_image")).split('"')[11]
        print(url_thumb)
        dominant_color = call.get_dominant_color(url_thumb)
    except:
        dominant_color = [0,0,0]
    r = dominant_color[0]
    g = dominant_color[1]
    b = dominant_color[2]

    return found, urlbasic, urlchapter, title, r, g, b


# Manga Clash

def getMangaClash(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay, id_guild):
    '''
        Thumbnail:  Y
        CHAPTER_NUMBER: Y
        URL_CHAPTER: Y
        CHECK_RELEASES: Y
    '''

    # Now get the time of release and if it already was released today or not
    try:
        web = req.get(url=f"{urlbasic}")
        menu_soup = bs(web.content, features="html.parser")
        chapter_text = (menu_soup.find("li", class_="wp-manga-chapter"))
        chapter_text = str(chapter_text.find("a"))
        chapter_text = chapter_text.split(">")[1]
        chapter_number = float(chapter_text.replace("</a", "").split(" ")[1])
        # now we have chapter_number

        # Mow I need the second chapter release date

        chapter_second = str(menu_soup.find_all("li", class_="wp-manga-chapter")[1])
        chapter_second = chapter_second.split('>')[5]
        chapter_second = chapter_second.split('<')[0]
        date_text = chapter_second

        # Returns the time until release
        until_release = call.getTime(rHour, rMin, rDay)

        # Now I will add the number of chapter to the url of chapter
        if chapter_number == int(chapter_number):
            urlchapter = str(urlchapter) + f'{int(chapter_number)}/'
            # It is a full number
        else:
            m_chapter_number = str(chapter_number).replace(".", '-')
            urlchapter = str(urlchapter) + f'{m_chapter_number}/'
        # Now I have the URL for the chapter

        # now I need the chapter_thumbnail
        thumbnail_text = (menu_soup.find("div", class_="summary_image"))
        thumbnail_text = str(thumbnail_text.find("img")).split('"')[5]
        url_thumbnail = thumbnail_text

        next_chapter = chapter_number + 1

        last_chapters = {}
        with open('server_latest', 'r', errors='ignore') as r_sl:
            if r_sl is not None:
                for line in r_sl:
                    if line is not None:
                        line_ = line.split('-')
                        if line[0] != ' \n':
                            if line_[0] == id_guild:
                                last_chapters.setdefault(line_[1], f'{line_[2]}')

        # Check if the last_chapters has the  current chapter number, if does it has not been released yet

        if last_chapters[Title] == chapter_number:
            released = False
        else:
            released = True

        if until_release[1] is True and released is True:
            message_release = f'The Chapter {int(next_chapter)} is being translated \n or is on break or has random releases'
        else:
            message_release = f'The Chapter {next_chapter} will be released in {until_release[0]}'
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                              description=f"The Chapter {chapter_number} \n " + message_release + f"\n Link to latest chapter: {urlchapter}",
                              color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{url_thumbnail}")
    except Exception as e:
        print(f'Error of MangaClash {Title}: {e}')

    return embed, chapter_number


def getMangaClashReleased(Title, urlbasic, urlchapter, r1, g, b, id_channel, id_guild):
    '''
        Thumbnail:  Y
        CHAPTER_NUMBER: Y
        URL_CHAPTER: Y
        CHECK_RELEASES: Y
    '''

    # Now get the time of release and if it already was released today or not
    subscription = []
    subscription_other = []
    content = []
    with open('server_release_ping', 'r', errors='ignore') as f:
        for line in f:
            splited = line.split("-")
            if splited[0] == id_guild:
                if splited[1] == Title:
                    # Now I just need to get the list of player
                    users = splited[2].replace("[", "")
                    users = users.replace("]", "")
                    users = users.replace("'", '')
                    users = users.replace("\\n", '')
                    users = users.replace("\n", '')
                    users = users.replace(" ", '')
                    users = users.replace("  ", '')
                    users = users.split(",")
                    subscription = users
                else:
                    subscription_other.append(line)
            else:
                subscription_other.append(line)

    web = req.get(url=f"{urlbasic}")
    menu_soup = bs(web.content, features="html.parser")
    chapter_text = (menu_soup.find("li", class_="wp-manga-chapter"))
    chapter_text = str(chapter_text.find("a"))
    chapter_text = chapter_text.split(">")[1]
    chapter_number = float(chapter_text.replace("</a", "").split(" ")[1])
    # now we have chapter_number

    # Now I will add the number of chapter to the url of chapter
    if chapter_number == int(chapter_number):
        urlchapter = str(urlchapter) + f'{int(chapter_number)}/'
        # It is a full number
    else:
        m_chapter_number = str(chapter_number).replace(".", '-')
        urlchapter = str(urlchapter) + f'{m_chapter_number}/'
    # Now I have the URL for the chapter

    # now I need the chapter_thumbnail
    thumbnail_text = (menu_soup.find("div", class_="summary_image"))
    thumbnail_text = str(thumbnail_text.find("img")).split('"')[5]
    url_thumbnail = thumbnail_text

    last_chapters = {}
    content_new = []
    content_servers = []
    content_new_ = f'{id_guild}-{Title}-{chapter_number}'
    content_new.append(content_new_)
    # Now get the time of release and if it already was released today or not
    with open('server_latest', 'r', errors='ignore') as r_sl:
        if r_sl is not None:
            for line in r_sl:
                if line is not None:
                    line_ = line.split('-')
                    if line[0] != ' \n':
                        if line_[0] == id_guild:
                            content_element = f'{line_[0]}-{(line_[1])}-{(line_[2])}'
                            content.append(content_element)
                            last_chapters.setdefault(line_[1], f'{line_[2]}')
                        else:
                            if str(line) != ' \n':
                                content_element = f'{line_[0]}-{(line_[1])}-{(line_[2])}'
                                content_servers.append(content_element)
                # Title Source  url  url_chapter r g b rHour rMinute rDay
    new = False
    if last_chapters.keys().__contains__(Title):
        chapter_last_number = last_chapters[Title]
        message_release = f"The Chapters {chapter_number} was released!"
    else:
        new = True
        message_release = f"The {Title} was added to existing bookmarks!"
        chapter_last_number = float(chapter_number) - 1

    released = False
    if float(chapter_number) > float(chapter_last_number):
        released = True
        # Now I have the list of all released chapters

    if new:
        with open('server_release_ping', 'w') as write:
            subscription.append(f'{id_guild}-{Title}-[]')
            for subs in subscription:
                write.write(f'{subs} \n')
            for subs in subscription_other:
                write.write(subs)
    # Its more than 1 chapter
    if released:
        with open('server_latest', 'w', errors='ignore') as wf:
            # Check if there are some that have to be updated
            for line in content:
                for line_new in content_new:
                    id_g_new = line_new.split("-")[0]
                    id_g = line.split("-")[0]
                    if id_g_new == id_g:
                        # found the same server
                        # Now I need to check for the Title
                        title_new = line_new.split("-")[1]
                        title_ = line.split("-")[1]
                        if title_ == title_new:
                            # Its the same manga! so delete the old one
                            content.remove(line)
            released = True
            # Write it down
            for c in content_new:
                wf.write(c + " \n")
            for c in content:
                if not c.__contains__('\n'):
                    wf.write(c + " \n")
                else:
                    wf.write(c)
            for c in content_servers:
                if not c.__contains__('\n'):
                    wf.write(c + " \n")
                else:
                    wf.write(c)
    if new is False:
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                              description=f"{message_release} \n Link to the chapter: {urlchapter}",
                              color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{url_thumbnail}")
    else:
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                              description=f"{message_release} \n Link to the chapter: {urlchapter}",
                              color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{url_thumbnail}")

    return released, embed, subscription, chapter_number
    # New chapter was RELEASED!!!!


def getAquaManga(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay):
    web = req.get(url=urlbasic)
    soup = bs(web.content, features="html.parser")
    chapter_text = (soup.find("li", class_="wp-manga-chapter"))
    print(chapter_text)


def getAquaMangaReleased(Title, urlbasic, urlchapter, r1, g, b):
    print("")


# Luminous Scans

def getLuminousScansReleased(Title, urlbasic, urlchapter, r1, g, b, id_channel, id_guild):
    # We get the soup of the website
    # urlbasic = 'https://luminousscans.com/series/1653732347-fff-class-trash-hero/'
    web = req.get(url=urlbasic)
    soup = bs(web.content, features="html.parser")
    content = web.content
    # Now we split it at the epcurlast class and split it again so we get the Chapter {number}
    chapter_text = str(content).split('epcurlast')
    chapter_text = chapter_text[1].split('<')[0].replace('">', '')

    chapter_num = float(chapter_text.split()[1])

    #
    # Url chapter
    urlchapter = urlchapter + f'{int(chapter_num)}/'

    # I will get the picture from the website as well
    thumb_url = str(soup.find('div', class_='thumb')).split()[15].split('"')[1]

    doFiles = call.doReleased(id_guild, Title, chapter_num, urlbasic, urlchapter, r1, g, b, thumb_url)
    released = doFiles[0]
    embed = doFiles[1]
    subscription = doFiles[2]

    return released, embed, subscription, chapter_num


def getLuminousScans(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay, id_guild):
    # We get the soup of the website
    # urlbasic = 'https://luminousscans.com/series/1653732347-fff-class-trash-hero/'
    web = req.get(url=urlbasic)
    soup = bs(web.content, features="html.parser")
    content = web.content
    # Now we split it at the epcurlast class and split it again so we get the Chapter {number}
    chapter_text = str(content).split('epcurlast')
    chapter_text = chapter_text[1].split('<')[0].replace('">', '')

    chapter_num = float(chapter_text.split()[1])

    #
    # Url chapter
    urlchapter = urlchapter + f'{int(chapter_num)}/'

    # I will get the picture from the website as well
    thumb_url = str(soup.find('div', class_='thumb')).split()[15].split('"')[1]

    docheck = call.doCheck(id_guild, Title, chapter_num, rHour, rMin, rDay, urlbasic, urlchapter, thumb_url, r1, g, b)
    embed = docheck

    return embed, chapter_num


# MangaKakalot

def getMangaKakalot(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay, id_guild):
    urlbasic = 'https://readmanganato.com/manga-ki987365'
    web = req.get(url=urlbasic)
    soup = bs(web.content, features="html.parser")
    chapter_num = str(soup.find("a", class_='chapter-name text-nowrap')).split('"')[8].replace('>Chapter ', '').replace(
        '</a>', '')

    # Now I need to do the chapter url
    urlchapter = urlchapter + f'{int(chapter_num)}'

    # Now I need to get thumbnail
    thumb_url = str(soup.find('span', class_='info-image')).split('"')[9]

    embed = call.doCheck(id_guild, Title, chapter_num, rHour, rMin, rDay, urlbasic, urlchapter, thumb_url, r1, g, b)

    return embed, chapter_num


def getMangaKakalotReleased(Title, urlbasic, urlchapter, r1, g, b, id_channel, id_guild):
    urlbasic = 'https://readmanganato.com/manga-ki987365'
    web = req.get(url=urlbasic)
    soup = bs(web.content, features="html.parser")
    chapter_num = float(
        str(soup.find("a", class_='chapter-name text-nowrap')).split('"')[8].replace('>Chapter ', '').replace('</a>',
                                                                                                              ''))
    # Now I need to get thumbnail
    thumb_url = str(soup.find('span', class_='info-image')).split('"')[9]

    # Now I need to do the chapter url
    urlchapter = urlchapter + f'{int(chapter_num)}'

    # Now I need to get the server_latest and server_release_ping
    doFiles = call.doReleased(id_guild, Title, chapter_num, urlbasic, urlchapter, r1, g, b, thumb_url)
    released = doFiles[0]
    embed = doFiles[1]
    subscription = doFiles[2]

    return released, embed, subscription, chapter_num


# 247Manga

def get247Manga(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay, id_guild):
    print("")


def get247MangaReleased(Title, urlbasic, urlchapter, r1, g, b):
    print("")


# Webtoons.com

def getWebtoons(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay):
    print("")


def getWebtoonsReleased(Title, urlbasic, urlchapter, r1, g, b):
    print("")
