from datetime import datetime
import discord
from colorthief import ColorThief
from PIL import Image
import requests


def rewrite(file_name, manga_new, manga_other):
    with open(file_name, "w") as w:
        w.write(manga_new)
        for manga in manga_other:
            w.write(manga)


def doReleased(guild_ids, Title, chapter_num, urlbasic, urlchapter, r1, g, b, thumb_url, source):
    # I need to get subs
    # print(f"doReleased {guild_ids, Title, chapter_num, urlbasic, urlchapter, r1, g, b, thumb_url, source}")
    subs = []
    embed = ""
    # I will have guild_id-title as a key with list of subscribed users as a value
    with open("server_release_ping", "r") as read_srp:
        for line_srp in read_srp:
            split = line_srp.split("-+-")
            guild_id = split[0]
            title = split[1]
            # check if this is part of the subs we need
            # and if the title is the same
            if guild_ids.__contains__(guild_id) and Title == title:
                sub_users = split[2].replace("[", "").replace("]", "").replace("'", '').replace("\\n", '').replace("\n",
                                                                                                                   '').replace(
                    " ", '').replace("  ", '').split(",")
                subs = sub_users
    #print(subs)
    # ---------------

    # I need to get the latest chapters
    manga_latest = 0.0
    other_latest = []
    with open("server_latest", "r") as read_sl:
        for line_sl in read_sl:
            split_sl = line_sl.split("-+-")
            Source = split_sl[0]
            title = split_sl[1]
            number = split_sl[2]
            #   source == source
            if Source == source:
                #   title == Title
                if title == Title:
                    manga_latest = float(split_sl[2])
                else:
                    other_latest.append(f"{Source}-+-{title}-+-{number}")
            else:
                other_latest.append(line_sl)
    # ---------------




    if manga_latest == 0.0:
        # its new one
        # its a newer chapter guys so rewrite server_latest file
        rewrite("server_latest", f"{source}-+-{Title}-+-{chapter_num} \n", other_latest)
        released = False
    else:
        # it already exist
        # need to check if its newer chapter
        released = False
        if float(chapter_num) > manga_latest:
            print("-------------------------------")
            print(f"Released {Title} - {chapter_num}")
            print("-------------------------------")
            # its a newer chapter guys so rewrite server_latest file
            rewrite("server_latest", f"{source}-+-{Title}-+-{chapter_num} \n", other_latest)
            # print(f"doReleased {guild_ids, Title, chapter_num, urlbasic, urlchapter, r1, g, b, thumb_url, source} - {source}-{Title}-{chapter_num} - {other_latest}")
            released = True
            message_release = f'The Chapter {chapter_num} was released'
            embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                                  description=f"{message_release} \n Link to the chapter: {urlchapter}",
                                  color=discord.Color.from_rgb(r1, g, b))
            #embed.set_image(url=f"{thumb_url}")

    return released, embed, subs













    '''# get subscriptions
    subscription = []
    subscription_other = []
    content = []
    # There it will open the file and find the users that are meant to be informed about new chapter
    with open('server_release_ping', 'r', errors='ignore') as f:
        for line in f:
            splited = line.split("-")
            if splited[0] == id_guild:
                if splited[1] == Title:
                    # Now I just need to get the list of player
                    users = splited[2].replace("[", "").replace("]", "").replace("'", '').replace("\\n", '').replace(
                        "\n", '').replace(" ", '').replace("  ", '').split(",")
                    subscription = users
                else:
                    subscription_other.append(line)
            else:
                subscription_other.append(line)

    # get content
    last_chapters = {}
    content_new = []
    content_servers = []
    content_new_ = f'{id_guild}-{Title}-{chapter_num}'
    content_new.append(content_new_)
    # Now get the time of release and if it already was released today or not
    with open('server_latest', 'r', errors='ignore') as r_sl:
        if r_sl is not None:
            for line in r_sl:
                if line is not None:
                    line_ = line.split('-')
                    if line[0] != ' \n':
                        # Ineed to check if its the server we want
                        if line_[0] == id_guild:
                            content_element = f'{line_[0]}-{(line_[1])}-{(line_[2])}'
                            content.append(content_element)
                            last_chapters.setdefault(line_[1], f'{line_[2]}')
                        else:
                            if str(line) != ' \n':
                                content_element = f'{line_[0]}-{(line_[1])}-{(line_[2])}'
                                content_servers.append(content_element)
    new = False
    released = False
    # Check if there is new episode
    if last_chapters.keys().__contains__(Title):
        if float(last_chapters.get(Title)) < float(chapter_num):
            released = True
    else:
        new = True
        released = True

    # Now I write the files if something new was released
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
        message_release = f'The Chapter {chapter_num} was released'
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                              description=f"{message_release} \n Link to the chapter: {urlchapter}",
                              color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{thumb_url}")
    else:
        message_release = f'The {Title} has been added to library'
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                              description=f"{message_release} \n Link to the chapter: {urlchapter}",
                              color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{thumb_url}")
    return released, embed, subscription'''


def doCheck(id_guild, Title, chapter_num, rHour, rMin, rDay, urlbasic, urlchapter, thumb_url, r1, g, b):
    # get subscriptions
    subscription = []
    subscription_other = []
    content = []
    # There it will open the file and find the users that are meant to be informed about new chapter
    with open('server_release_ping', 'r', errors='ignore') as f:
        for line in f:
            splited = line.split("-+-")
            if splited[0] == id_guild:
                if splited[1] == Title:
                    # Now I just need to get the list of player
                    users = splited[2].replace("[", "").replace("]", "").replace("'", '').replace("\\n", '').replace(
                        "\n", '').replace(" ", '').replace("  ", '').split(",")
                    subscription = users
                else:
                    subscription_other.append(line)
            else:
                subscription_other.append(line)

    # get content
    last_chapters = {}
    content_new = []
    content_servers = []
    content_new_ = f'{id_guild}-{Title}-{chapter_num}'
    content_new.append(content_new_)
    # Now get the time of release and if it already was released today or not
    with open('server_latest', 'r', errors='ignore') as r_sl:
        if r_sl is not None:
            for line in r_sl:
                if line is not None:
                    line_ = line.split('-+-')
                    if line[0] != ' \n':
                        if line_[0] == id_guild:
                            content_element = f'{line_[0]}-+-{(line_[1])}-+-{(line_[2])}'
                            content.append(content_element)
                            last_chapters.setdefault(line_[1], f'{line_[2]}')
                        else:
                            if str(line) != ' \n':
                                content_element = f'{line_[0]}-+-{(line_[1])}-+-{(line_[2])}'
                                content_servers.append(content_element)
    new = False
    released = False
    # Check if there is new episode
    if last_chapters.keys().__contains__(Title):
        if float(last_chapters.get(Title)) < float(chapter_num):
            released = True
    else:
        new = True
        released = True

    # Now I need to get the time and know when its gonna be released
    until_release = getTime(rHour, rMin, rDay)

    if until_release[1] is True and released is True:
        message_release = f'The Chapter {chapter_num} is being translated \n or is on break or has random releases'
    else:
        message_release = f'The Chapter {(float(chapter_num) + 1)} will be released in {until_release[0]}'
    embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                          description=f"The Chapter {chapter_num} \n " + message_release + f"\n Link to latest chapter: {urlchapter}",
                          color=discord.Color.from_rgb(r1, g, b))
    embed.set_image(url=f"{thumb_url}")

    return embed


def getTime(rHour, rMinute, rDay):
    date = datetime.today().strftime("%Y-%m-%d")
    temp = datetime.today().weekday()

    day = datetime.today().weekday()
    # Released on Friday at 18:00 / 6PM
    release = 18
    hour = int(datetime.today().strftime("%H")) * 60 * 60
    min = int(datetime.today().strftime("%M")) * 60
    sec = int(datetime.today().strftime("%S"))
    time_sec = hour + min + sec + day * 24 * 60 * 60
    # Time in seconds until release
    countdown_left = int((rHour * 60 * 60 + rMinute * 60 - time_sec) / 60 + rDay * 24 * 60)
    negative = True
    if countdown_left > 0:
        negative = False

    if countdown_left <= 0:
        countdown_left = countdown_left + 7 * 24 * 60
    if abs(countdown_left) > (24 * 60):
        days_r = int(countdown_left / 60 / 24)
        countdown_left = countdown_left - days_r * 24 * 60
    else:
        days_r = 0
    if abs(countdown_left) > 60:
        hour_r = int(countdown_left / 60)
        countdown_left = countdown_left - hour_r * 60
    else:
        hour_r = 0
    min_r = countdown_left

    message_finall = f"{days_r} days  {hour_r} hours {min_r} minutes"

    return message_finall, negative


def get_dominant_color(url_image, palette_size=16):
    im = Image.open(requests.get(url_image, stream=True).raw)
    img = im.copy()

    img.convert('RGB')

    width, height = img.size
    r_total = 0
    g_total = 0
    b_total = 0

    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x, y))
            r_total += r
            g_total += g
            b_total += b
    # print(r_total/(width*height), g_total/(width*height), b_total/(width*height))

    #               R                      G                        B
    return round(r_total / (width * height)), round(g_total / (width * height)), round(b_total / (width * height))


def add_manga(id_guild, id_channel, cmd, title, source, url, r, g, b, rHour, rMin, rDay):
    # I will first need to read the channel_listed
    exist_manga = ""
    other_manga = []
    contained = False
    with open("channel_listed", "r") as read_cl:
        for line_cl in read_cl:
            if line_cl != "\n":
                # in channel_listed I use two spaces as a separator, cuz I use spaces in titles
                split_cl = line_cl.split("  ")
                if url == split_cl[5] and title == split_cl[3]:
                    print("exists")
                    # it has the same url and title so it already exist, I just need to add it to the list of guild and channel ids if its not alerady there
                    guild_ids = split_cl[0].replace("'", "").replace("[", "").replace("]", "").split(",")
                    channel_ids = split_cl[1].replace("'", "").replace("[", "").replace("]", "").split(",")
                    print(guild_ids, channel_ids)
                    if guild_ids.__contains__(id_guild):
                        # It already is added so just set contained True and return it and dont do anythin else
                        contained = True
                else:
                    other_manga.append(line_cl)

    if contained is False:
        if exist_manga == "":
            # Manga was not found, so it is a new one
            guild_id_list = []
            guild_id_list.append(id_guild)
            channel_id_list = []
            channel_id_list.append(id_channel)
            exist_manga = f"{guild_id_list}  {channel_id_list}  {cmd}  {title}  {source}  {url}  {r}  {g}  {b}  {rHour}  {rMin}  {rDay}  \n"
        else:
            # Manga was found, so I will just edit it
            print("exists")

        # Its written down in channel listed
        with open("channel_listed", "w") as write_cl:
            write_cl.write(exist_manga)
            for manga_register in other_manga:
                write_cl.write(manga_register)

        # server_release_ping
        if True:
            # This will be done either way, if it already exists or its new
            # I will add it to server_release ping
            srp_pings = []
            with open("server_release_ping", "r") as read_srp:
                for line_srp in read_srp:
                    srp_pings.append(line_srp)
            # I have the list of the sr pings so I will write them back with the new one added
            empty = []
            new_ping = f"{id_guild}-+-{title}-+-{empty} \n"
            with open("server_release_ping", "w") as write_srp:
                write_srp.write(new_ping)
                for ping in srp_pings:
                    write_srp.write(ping)
    return contained
