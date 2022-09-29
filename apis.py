import nextcord
import requests as req
from bs4 import BeautifulSoup as bs
import callables as call

headers = {
    'User-Agent': 'Mozilla/5.0'}


def getReleases(source, Title, urlbasic, r1, g, b, id_guild):
    try:
        r = []
        if source == "ReaperScans":
            r = getReaperScansReleased(Title, urlbasic, r1, g, b, id_guild, source)
            #print("Reaper")
        elif source == " MangaClash" or source == "MangaClash" or source == "  MangaClash":
            r = getMangaClashReleased(Title, urlbasic, r1, g, b, id_guild, source)
            #print("MangaClash")
        elif source == "LuminousScans":
            r = getLuminousScansReleased(Title, urlbasic, r1, g, b, id_guild, source)
            #print("LuminousScans")
        elif source == "MangaKakalot":
            r = getMangaKakalotReleased(Title, urlbasic, r1, g, b, id_guild, source)
            #print("Kakalot")

        released = r[0]
        if released is True:
            embed = r[1]
            subscription = r[2]
            chapter_number = r[3]
            urlbasic = r[4]
            urlchapter = r[5]
            url_thumb = r[9]
            chapter_num = r[6]
            message_release = r[7]
            sources_announced_already = r[8]
            return released, embed, subscription, chapter_number, urlbasic, urlchapter, chapter_num, message_release, sources_announced_already, url_thumb
        else:
            embed = ""
            return released, embed
    except:
        return False, ""


# Reaper Scans
def getReaperScans(Title, urlbasic, r1, g, b, rHour, rMin, rDay, id_guild):
    urlchapter = urlbasic + "chapter-"
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


def getReaperScansReleased(Title, urlbasic, r1, g, b, guild_ids, source):
    urlchapter = urlbasic + "chapter-"
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
    if str(chapter_number).split('.')[1] != '0':
        chapter_number_text = str(chapter_number).split('.')[0] + '-' + str(chapter_number).split('.')[1]
    else:
        chapter_number_text = str(int(chapter_number_text))

    urlchapter += f'{chapter_number_text}/'

    releaseR = call.doReleased(guild_ids, Title, chapter_number, urlbasic, urlchapter, r1, g, b, url_thumbnail, source)
    if releaseR[0] is True:
        released = releaseR[0]
        embed = releaseR[1]
        subscription = releaseR[2]
        urlbasic = releaseR[3]
        urlchapter = releaseR[4]
        chapter_num = releaseR[5]
        message_release = releaseR[6]
        sources_announced_already = releaseR[7]
        return released, embed, subscription, chapter_number, urlbasic, urlchapter, chapter_num, message_release,sources_announced_already, url_thumbnail
    else:
        released = releaseR[0]
        embed = ""
        return released, embed


def searchReaperScans(Title):
    try:
        title = str(Title).lower().replace(" ", "-").replace("’", "")
        title = title.replace("---manhwa", "-manhwa")
        url = f"https://reaperscans.com/series/{title}/"
        web = req.get(url, headers=headers)
        soup = bs(web.content, features="html.parser")
        mnhwornvl = True
        type = str(soup.find("div", class_="post-title")).split(">")
        type = type[2].replace("</span", "")
        print((type.lower()).__contains__("novel"))
        if (type.lower()).__contains__("novel"):
            mnhwornvl = False
        found = False
        urlbasic = ""
        r = 0
        g = 0
        b = 0
        cmd = ""

        title = ""
        urlbasic = ""
        urlchapter = ""
        # I am looking for a div with class post-title
        if soup.find("div", class_="post-title") is not None:
            # I checked if there is a 404 not found picture, so if there isnt, it was found
            found = True
            urlbasic = url
            urlchapter = f"{urlbasic}chapter-"
        else:
            found = False
        # Check if its a novel or not, True = Manhwa..., False = Novel...
        if mnhwornvl is True:
            # I will find the title now,
            try:
                title = str(soup.find("div", class_="post-title")).split(">")[4].split("<")[0].replace("\n",
                                                                                                       "").replace(
                    "\t",
                    "")
                #title = title[0:(len(title)-20)]
                title = title.replace("                    ","")[0:(len(title)-1)]
            except:
                title = "Title Not Found"
            # I will need to get RGB of the thumb
            # so first I get the thumbnail
            try:
                url_thumb = str(soup.find("div", class_="summary_image")).split('"')[11]
                dominant_color = call.get_dominant_color(url_thumb)
            except:
                dominant_color = [0, 0, 0]
            r = dominant_color[0]
            g = dominant_color[1]
            b = dominant_color[2]

            try:
                # I will get each first two letters from the name and set it as cmd
                cmd = ""
                for ch in (title.split()):
                    if ch[0] != "–":
                        cmd += ch[0].lower()
                    try:
                        if ch[1] != "–":
                            cmd += ch[1].lower()
                    except:
                        cmd += ""
            except:
                cmd = ""
        error = False
        print(found, urlbasic, title, r, g, b, cmd, mnhwornvl, error)
        return found, urlbasic, title, r, g, b, cmd, mnhwornvl, error
    except:
        return False, 0, 1, 2, 3, 4, 5, 6, True


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
                        line_ = line.split('-+-')
                        if line[0] != ' \n':
                            if line_[0] == id_guild:
                                last_chapters.setdefault(line_[1], f'{line_[2]}')

        # Check if the last_chapters has the  current chapter number, if does it has not been released yet
        last_chapter = last_chapters[Title]
        if last_chapter == chapter_number:
            released = False
        else:
            released = True

        if until_release[1] is True and released is True:
            message_release = f'The Chapter {int(next_chapter)} is being translated \n or is on break or has random releases'
        else:
            #Check if there was only one chapter released
            chapters = []
            chapters.append(chapter_number)
            if (last_chapter - chapter_number) != 0:
                for num in range(int(last_chapter), int(chapter_number)):
                    chapters.append(num)
            chapters = chapters.replace("[", "").replace(" ", "").replace("]", "")
            message_release = f'The Chapter {next_chapter} will be released in {until_release[0]}'
        embed = nextcord.Embed(title=f"{Title}", url=f"{urlbasic}",
                              description=f"The Chapter {str(chapters)} \n " + message_release + f"\n Link to latest chapter: {urlchapter}",
                              color=nextcord.Color.from_rgb(r1, g, b))
    except Exception as e:
        print(f'Error of MangaClash {Title}: {e}')

    return embed, chapter_number


def getMangaClashReleased(Title, urlbasic, r1, g, b, guild_ids, source):
    # I got the web, cuz I need chap number
    web = req.get(url=f"{urlbasic}")
    menu_soup = bs(web.content, features="html.parser")
    chapter_text = (menu_soup.find("li", class_="wp-manga-chapter"))
    chapter_text = str(chapter_text.find("a"))
    chapter_text = chapter_text.split(">")[1]
    chapter_number = float(chapter_text.replace("</a", "").split(" ")[1])
    # now we have chapter_number

    # urlchapter:
    urlchapter = urlbasic + "/chapter-" + str(int(chapter_number)) + "/"

    # now I need the chapter_thumbnail

    text_thumbnail = (menu_soup.find("div", class_="summary_image"))
    url_thumbnail = str(text_thumbnail.find("a")).split('"')
    if  not (url_thumbnail[9].__contains__("http")):
        url_thumbnail = url_thumbnail[7]
    else:
        url_thumbnail = url_thumbnail[9]

    releaseR = call.doReleased(guild_ids, Title, chapter_number, urlbasic, urlchapter, r1, g, b, url_thumbnail, source, )
    if releaseR[0] is True:
        released = releaseR[0]
        embed = releaseR[1]
        subscription = releaseR[2]
        urlbasic = releaseR[3]
        urlchapter = releaseR[4]
        chapter_num = releaseR[5]
        message_release = releaseR[6]
        sources_announced_already = releaseR[7]
        return released, embed, subscription, chapter_number, urlbasic, urlchapter, chapter_num, message_release, sources_announced_already, url_thumbnail
    else:
        released = releaseR[0]
        embed = ""
        return released, embed


def searchMangaClash(Title):
    try:
        # Checking if user provided url or a Title
        if str(Title).__contains__("https://mangaclash.com/"):
            url = Title
            web = req.get(url, headers=headers)
            soup = bs(web.content, features="html.parser")
        else:
            title = str(Title).lower().replace(" ", "-").replace("’", "")
            title = title.replace("---manhwa", "-manhwa")
            # https://mangaclash.com/manga-genre/manhwa/
            url = f"https://mangaclash.com/manga/{title}/"
            web = req.get(url, headers=headers)
            url = web.url
            soup = bs(web.content, features="html.parser")
        found = False
        urlbasic = ""
        r = 0
        g = 0
        b = 0
        cmd = ""
        mnhwornvl = True
        title = ""
        urlbasic = ""
        urlchapter = ""
        # I am looking for a div with class post-title
        if soup.find("div", class_="post-title") is not None:
            # I checked if there is a 404 not found picture, so if there isnt, it was found
            found = True
            urlbasic = url
            urlchapter = f"{urlbasic}chapter-"
        else:
            found = False
        # Check if its a novel or not, True = Manhwa..., False = Novel...

        # I will find the title now,
        try:
            title = str(soup.find("div", class_="post-title"))
            title = title.split(">")[2].replace("\n", "").replace("</h1", "").replace("’", "")
        except:
            title = "Title Not Found"
        title = title[0:(len(title)-1)]
        # I need to remove the spaces at the end of the title
        enough = False
        # I will need to get RGB of the thumb
        # so first I get the thumbnail
        try:
            text_thumbnail = (soup.find("div", class_="summary_image"))
            url_thumb = str(text_thumbnail.find("a")).split('"')
            if not (url_thumb[9].__contains__("http")):
                url_thumb = url_thumb[7]
            else:
                url_thumb = url_thumb[9]

            dominant_color = call.get_dominant_color(url_thumb)
        except:
            dominant_color = [0, 0, 0]
        r = dominant_color[0]
        g = dominant_color[1]
        b = dominant_color[2]

        try:
            # I will get each first two letters from the name and set it as cmd
            cmd = ""
            for ch in (Title.split()):
                if ch[0] != "–":
                    cmd += ch[0].lower()
                try:
                    if ch[1] != "–":
                        cmd += ch[1].lower()
                except:
                    cmd += ""
        except:
            cmd = ""
        error = False
    except:
        error = True


    return found, urlbasic, title, r, g, b, cmd, mnhwornvl, error, url_thumb


def getAquaManga(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay):
    web = req.get(url=urlbasic)
    soup = bs(web.content, features="html.parser")
    chapter_text = (soup.find("li", class_="wp-manga-chapter"))
    #print(chapter_text)


def getAquaMangaReleased(Title, urlbasic, urlchapter, r1, g, b):
    print("")


# Luminous Scans

def getLuminousScansReleased(Title, urlbasic, r1, g, b, id_guild, source):
    # We get the soup of the website
    # urlbasic = 'https://luminousscans.com/series/1653732347-fff-class-trash-hero/'
    web = req.get(url=urlbasic, headers=headers)
    soup = bs(web.content, features="html.parser")
    content = web.content
    # Now we split it at the epcurlast class and split it again so we get the Chapter {number}
    chapter_text = str(content).split('epcurlast')
    chapter_text = chapter_text[1].split('<')[0].replace('">', '')

    chapter_number = float(chapter_text.split()[1])

    #
    # Url chapter
    urlchapter = urlbasic + f'chapter-{int(chapter_number)}/'

    # I will get the picture from the website as well
    try:
        thumb_url = str(soup.find('div', class_='thumb')).split('"')[19]
    except:
        thumb_url = ""
    #print(f"{thumb_url} - url")
    #(guild_ids, Title, chapter_num, urlbasic, urlchapter, r1, g, b, thumb_url, source)
    releaseR = call.doReleased(id_guild, Title, chapter_number, urlbasic, urlchapter, r1, g, b, thumb_url, source)
    if releaseR[0] is True:
        released = releaseR[0]
        embed = releaseR[1]
        subscription = releaseR[2]
        urlbasic = releaseR[3]
        urlchapter = releaseR[4]
        chapter_num = releaseR[5]
        message_release = releaseR[6]
        sources_announced_already = releaseR[7]
        return released, embed, subscription, chapter_number, urlbasic, urlchapter, chapter_num, message_release,sources_announced_already, thumb_url
    else:
        released = releaseR[0]
        embed = ""
        return released, embed


def getLuminousScans(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay, id_guild):
    # We get the soup of the website
    # urlbasic = 'https://luminousscans.com/series/1653732347-fff-class-trash-hero/'
    web = req.get(url=urlbasic)
    soup = bs(web.content, features="html.parser", headers=headers)
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


def searchLuminousScans(Title):
    try:
        # Checking if user provided url or a Title
        if str(Title).__contains__("https://luminousscans.com/series/"):
            url = Title
            web = req.get(url, headers=headers)
            soup = bs(web.content, features="html.parser")
        else:
            title = str(Title).lower().replace(" ", "-").replace("’", "")
            title = title.replace("---manhwa", "-manhwa")
            url = f"https://luminousscans.com/series/{title}/"
            web = req.get(url, headers=headers)
            soup = bs(web.content, features="html.parser")

        mnhwornvl = True
        try:
            type = str(soup.find("div", class_="post-title")).split(">")
            type = type[2].replace("</span", "")
            if (type.lower()).__contains__("novel"):
                mnhwornvl = False
        except:
            mnhwornvl = True
        found = False
        urlbasic = ""
        r = 0
        g = 0
        b = 0
        cmd = ""

        title = ""
        urlbasic = ""
        urlchapter = ""
        # I am looking for a div with class post-title
        #print(soup.find("h1", class_="entry-title"))
        if soup.find("h1", class_="entry-title") is not None:
            # I checked if there is a 404 not found picture, so if there isnt, it was found
            found = True
            urlbasic = url
            urlchapter = f"{urlbasic}chapter-"
        else:
            found = False
        # Check if its a novel or not, True = Manhwa..., False = Novel...
        if mnhwornvl is True:
            # I will find the title now,
            try:
                title = str(soup.find("h1", class_="entry-title")).split(">")[1].split("<")[0].replace("\n","").replace("\t","")
            except:
                title = "Title Not Found"
            # I will need to get RGB of the thumb
            # so first I get the thumbnail
            try:
                url_thumb = str(soup.find('div', class_='thumb')).split('"')[19]
                #print(url_thumb)
                dominant_color = call.get_dominant_color(url_thumb)
            except:
                dominant_color = [0, 0, 0]
            r = dominant_color[0]
            g = dominant_color[1]
            b = dominant_color[2]

            try:
                # I will get each first two letters from the name and set it as cmd
                cmd = ""
                for ch in (title.split()):
                    if ch[0] != "–":
                        cmd += ch[0].lower()
                    try:
                        if ch[1] != "–":
                            cmd += ch[1].lower()
                    except:
                        cmd += ""
            except:
                cmd = ""
        error = False
        return found, urlbasic, title, r, g, b, cmd, mnhwornvl, error
    except:
        return False, 0, 1, 2, 3, 4, 5, 6, True


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


def getMangaKakalotReleased(Title, urlbasic, urlchapter, r1, g, b, id_guild):
    urlbasic = 'https://mangakakalot.com/manga/{'
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

    return released, embed, subscription, chapter_num, thumb_url


# idk how their naming sense works tbh
def searchMangaKakalot(Title):
    global url_thumb
    try:
        # Checking if user provided url or a Title
        if str(Title).__contains__("mangakakalot."):
            url = Title
            web = req.get(url, headers=headers)
            soup = bs(web.content, features="html.parser")
            print(web.status_code)
        else:
            title = str(Title).lower().replace(" ", "-").replace("’", "")
            title = title.replace("---manhwa", "-manhwa")
            url = f"https://mangakakalot.com/manga/{title}/"
            web = req.get(url, headers=headers)
            soup = bs(web.content, features="html.parser")
            print(web.status_code)
        urlbasic = url

        # I am looking for a div with class post-title
        if soup.find("ul", class_="manga-info-text") is not None:
            # I checked if there is a 404 not found picture, so if there isnt, it was found
            found = True
            urlbasic = url
        else:
            found = False
        # Check if its a novel or not, True = Manhwa..., False = Novel...
        if True:
            # I will find the title now,
            try:
                title = str(soup.find("ul", class_="manga-info-text")).split(">")[3].split("<")[0].replace("\n",
                                                                                                       "").replace(
                    "\t",
                    "")
            except:
                title = "Title Not Found"
            # I will need to get RGB of the thumb
            # so first I get the thumbnail
            try:
                url_thumb = str(soup.find("div", class_="summary_image")).split('"')[11]
                dominant_color = call.get_dominant_color(url_thumb)
            except:
                dominant_color = [0, 0, 0]
            r = dominant_color[0]
            g = dominant_color[1]
            b = dominant_color[2]

            try:
                # I will get each first two letters from the name and set it as cmd
                cmd = ""
                for ch in (title.split()):
                    if ch[0] != "–":
                        cmd += ch[0].lower()
                    try:
                        if ch[1] != "–":
                            cmd += ch[1].lower()
                    except:
                        cmd += ""
            except:
                cmd = ""
        error = False
        print(found, urlbasic, title, r, g, b, cmd, True, error)
        return found, urlbasic, title, r, g, b, cmd, True, error, url_thumb
    except:
        return False, 0, 1, 2, 3, 4, 5, 6, True


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
