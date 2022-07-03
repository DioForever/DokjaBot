from datetime import datetime
import discord


def doReleased(id_guild, Title, chapter_num, urlbasic, urlchapter, r1, g, b, thumb_url):
    # get subscriptions
    subscription = []
    subscription_other = []
    content = []
    # There it will open the file and find the users that are meant to be informed about new chapter
    with open('server_release_ping', 'r', errors='ignore') as f:
        for line in f:
            splited = line.split("-")
            # Now I have [0] as [guild ids] string and [1] as title and [2] as [users ids] string
            # I need to make the string of guild ids to list
            gi_srp = splited[0].replace("[","").replace("]","").replace(" ","").split(",")
            found_gi_srp = False
            for gi in gi_srp:
                if found_gi_srp is False:
                    if id_guild == gi:
                        found_gi_srp = True
            if found_gi_srp:
                if splited[1] == Title:
                    # Now I just need to get the list of player
                    users = splited[2].replace("[", "").replace("]", "").replace("'", '').replace("\\n", '').replace("\n", '').replace(" ", '').replace("  ", '').split(",")
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
                    if line[0] != ' \n':
                        line_ = line.split('-')
                        # split the line to [0] string of [guild ids] [1] title and [2] the latest chapter
                        gi_sl = line_[0].replace("[", "").replace("]", "").replace(" ", "").replace("'","").split(",")
                        # I made gi_sl a list of [guild ids]
                        # I need to check if its the server we want
                        found_gi_sl = False
                        for gi in gi_sl:
                            if found_gi_sl is False:
                                if id_guild == gi:
                                    found_gi_sl = True
                        if found_gi_sl:
                            content_element = f'{gi_sl}-{(line_[1])}-{(line_[2])}'
                            content.append(content_element)
                            last_chapters.setdefault(line_[1], f'{line_[2]}')
                        else:
                            if str(line) != ' \n':
                                content_element = f'{gi_sl}-{(line_[1])}-{(line_[2])}'
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
            '''# Check if there are some that have to be updated
            for line in content:
                for line_new in content_new:
                    # ids_guilds-title-latest_chapter
                    id_g_new = line_new.split("-")[0]
                    id_g = line.split("-")[0]
                    if id_g_new == id_g:
                        # found the same server
                        # Now I need to check for the Title
                        title_new = line_new.split("-")[1]
                        title_ = line.split("-")[1]
                        if title_ == title_new:
                            # Its the same manga! so delete the old one
                            content.remove(line)'''
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
    return released, embed, subscription


def doCheck(id_guild, Title, chapter_num, rHour, rMin, rDay, urlbasic, urlchapter, thumb_url, r1, g, b):
    # get subscriptions
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
                    users = splited[2].replace("[", "").replace("]", "").replace("'", '').replace("\\n", '').replace("\n", '').replace(" ", '').replace("  ", '').split(",")
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