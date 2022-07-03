from datetime import datetime
import discord
import apis as api


#@tasks.loop(seconds=60)
async def chapterreleasecheck(bot, announced):
    # I need to wait till the bot is running
    await bot.wait_until_ready()
    channel_print = bot.get_channel(980509693329932338)
    start = datetime.now().strftime('%H:%M:%S')
    print(f'Refreshing releases status: Starting {start}')
    await channel_print.send(f'Refreshing releases status: Starting {start}')
    try:

        # I need to get the chapters latest from the server.latest
        chapters_released = {}
        with open('server_latest', 'r', errors='ignore') as r_sl:
            if r_sl is not None:
                for line in r_sl:
                    if line != "":
                        if line is not None:
                            line = line.split("-")
                            if line[0] != ' \n':
                                id_channel = line[0]
                                name_number = f'{line[1]}-{line[2]}'
                                chapters_released.setdefault(id_channel, name_number)

        # Now I need the channel_listed and check every one of them
        print(announced)
        await channel_print.send(announced)
        with open('channel_listed', 'r', errors='ignore') as r_cl:
            if r_cl is not None:
                for line in r_cl:
                    line = line.split("  ")
                    # split it so we get guild id, channel id, ect
                    id_guild = line[0].replace("[","").replace("]","").split(",")
                    # now I made it a list of server (guild ids) that want this manga to be announced
                    id_channel = line[1]
                    # now I made it a list of server channels (channel ids) that want this manga to be announced
                    title = line[3]
                    # Title is from the website its from
                    source = line[4].replace(" ", "")
                    # Source is the name of the source the manga is from example: ReaperScans, MangaClash, AsuraScans
                    url_basic = line[5]
                    # urlbasic is the url to the menu of the manga
                    url_chapter = line[6]
                    # urlchapter is the url to one of the chapters but removed the end
                    r = line[7]
                    g = line[8]
                    b = line[9]
                    # I saved the rgb to get the color of the embed
                    # Now I need to check the source and according to that I need to send the embed
                    try:
                        if source == "ReaperScans":
                            getReaperRelease = api.getReaperScansReleased(title, url_basic, url_chapter, int(r), int(g),
                                                                      int(b), id_channel,
                                                                      id_guild)
                            if announced.keys().__contains__(f'{id_guild}-{title}'):
                                if float(announced.get(f'{id_guild}-{title}')) < getReaperRelease[3]:
                                    if float(announced.get(f'{id_guild}-{title}')) < getReaperRelease[3]:
                                        # I will check the dm_ping file and see if they want dm
                                        dm_subs = []
                                        dm_other = []
                                        subscription_p = getReaperRelease[2].copy()
                                        with open('dm_ping', 'r') as r_dm:
                                            for line_dm in r_dm:
                                                split_dm = line_dm.split('-')
                                                guild_dm = split_dm[0]
                                                subs_dm = split_dm[1].split(',')
                                                if str(guild_dm) == str(id_guild):
                                                    for s in subs_dm:
                                                        n = s.replace("['", '').replace("']", '')
                                                        dm_subs.append(n)
                                                        if subscription_p.__contains__(n):
                                                            subscription_p.remove(n)
                                                else:
                                                    dm_other.append(line_dm)

                                        # -------
                                    channel = bot.get_channel(int(id_channel))
                                    embed = getReaperRelease[1]
                                    try:
                                        await channel.send(embed=embed)
                                    except:
                                        embed.set_image(url='')
                                        await channel.send(embed=embed)
                                    await channel.send(
                                        f'>>> Ping of The {title} {getReaperRelease[3]}: {subscription_p}',
                                        delete_after=300)
                                    announced[f'{id_guild}-{title}'] = float(getReaperRelease[3])
                                    print('------------------------------------')
                                    await channel_print.send('------------------------------------')
                                    print(f'{title} {getReaperRelease[3]}: {getReaperRelease[2]}')
                                    await channel_print.send(
                                        str(f'{title} {getReaperRelease[3]}: {getReaperRelease[2]}').replace('@', ''))
                                    print('------------------------------------')
                                    await channel_print.send('------------------------------------')

                                    # DM to the user
                                    chapter_num = getReaperRelease[3]
                                    server = bot.get_guild(int(id_guild))
                                    embed_user = discord.Embed(title=f"{title}", url=f"{url_basic}",
                                                               description=f"The Chapter {chapter_num} was released! \n"
                                                                           f" Link to the chapter: {url_chapter}{int(chapter_num)} \n"
                                                                           f" Server: {server}",
                                                               color=discord.Color.from_rgb(int(r), int(g), int(b)))

                                    # Now I have the dm sub ids
                                    subscription = getReaperRelease[2]

                                    for sub in subscription:
                                        if dm_subs.__contains__(sub):
                                            id = int(sub.replace('<@', '').replace('>', ''))
                                            user = await bot.fetch_user(id)
                                            await user.send(embed=embed_user)
                                    # --------------
                            else:
                                channel = bot.get_channel(int(id_channel))
                                embed = getReaperRelease[1]
                                try:
                                    await channel.send(embed=embed)
                                except:
                                    embed.set_image(url='')
                                    await channel.send(embed=embed)
                                await channel.send(
                                    f'>>> Ping of The {title} {getReaperRelease[3]}: {getReaperRelease[2]}',
                                    delete_after=300)
                                announced.setdefault(f'{id_guild}-{title}', float(getReaperRelease[3]))
                                print('------------------------------------')
                                await channel_print.send('------------------------------------')
                                print(f'{title} {getReaperRelease[3]}: {getReaperRelease[2]}')
                                await channel_print.send(
                                    str(f'{title} {getReaperRelease[3]}: {getReaperRelease[2]}').replace('@', ''))
                                print('------------------------------------')
                                await channel_print.send('------------------------------------')

                        elif source == "MangaClash":
                            getMangaClashRelease = api.getMangaClashReleased(title, url_basic, url_chapter, int(r), int(g),
                                                                         int(b), id_channel,
                                                                         id_guild)
                            if announced.keys().__contains__(f'{id_guild}-{title}'):
                                if float(announced.get(f'{id_guild}-{title}')) < getMangaClashRelease[3]:
                                    # I will check the dm_ping file and see if they want dm
                                    dm_subs = []
                                    dm_other = []
                                    subscription_p = getMangaClashRelease[2].copy()
                                    with open('dm_ping', 'r') as r_dm:
                                        for line_dm in r_dm:
                                            split_dm = line_dm.split('-')
                                            guild_dm = split_dm[0]
                                            subs_dm = split_dm[1].split(',')
                                            if str(guild_dm) == str(id_guild):
                                                for s in subs_dm:
                                                    n = s.replace("['", '').replace("']", '')
                                                    '''dm_subs.append(n)'''
                                                    if subscription_p.__contains__(n):
                                                        subscription_p.remove(n)
                                            else:
                                                dm_other.append(line_dm)

                                    # -------
                                    channel = bot.get_channel(int(id_channel))
                                    embed = getMangaClashRelease[1]
                                    try:
                                        await channel.send(embed=embed)
                                    except:
                                        embed.set_image(url='')
                                        await channel.send(embed=embed)
                                    await channel.send(
                                        f'>>> Ping of The {title} {getMangaClashRelease[3]}: {subscription_p}',
                                        delete_after=300)
                                    announced[f'{id_guild}-{title}'] = float(getMangaClashRelease[3])
                                    print('------------------------------------')
                                    await channel_print.send('------------------------------------')
                                    print(f'{title} {getMangaClashRelease[3]}: {getMangaClashRelease[2]}')
                                    await channel_print.send(
                                        str(f'{title} {getMangaClashRelease[3]}: {getMangaClashRelease[2]}').replace(
                                            '@', ''))
                                    print('------------------------------------')
                                    await channel_print.send('------------------------------------')

                                    # DM to the user
                                    chapter_num = getMangaClashRelease[3]
                                    server = bot.get_guild(int(id_guild))
                                    embed_user = discord.Embed(title=f"{title}", url=f"{url_basic}",
                                                               description=f"The Chapter {chapter_num} was released! \n"
                                                                           f" Link to the chapter: {url_chapter}{int(chapter_num)} \n"
                                                                           f" Server: {server}",
                                                               color=discord.Color.from_rgb(int(r), int(g), int(b)))

                                    # Now I have the dm sub ids
                                    subscription = getMangaClashRelease[2]

                                    for sub in subscription:
                                        if dm_subs.__contains__(sub):
                                            id = int(sub.replace('<@', '').replace('>', ''))
                                            user = await bot.fetch_user(id)
                                            await user.send(embed=embed_user)
                                    # --------------
                            else:
                                channel = bot.get_channel(int(id_channel))
                                embed = getMangaClashRelease[1]
                                try:
                                    await channel.send(embed=embed)
                                except:
                                    embed.set_image(url='')
                                    await channel.send(embed=embed)
                                await channel.send(
                                    f'>>> Ping of The {title} {getMangaClashRelease[3]}: {getMangaClashRelease[2]}',
                                    delete_after=300)
                                announced.setdefault(f'{id_guild}-{title}', float(getMangaClashRelease[3]))
                                print('------------------------------------')
                                await channel_print.send('------------------------------------')
                                print(f'{title} {getMangaClashRelease[3]}: {getMangaClashRelease[2]}')
                                await channel_print.send(
                                    str(f'{title} {getMangaClashRelease[3]}: {getMangaClashRelease[2]}').replace('@',
                                                                                                                 ''))
                                print('------------------------------------')
                                await channel_print.send('------------------------------------')
                        elif source == "LuminousScans":
                            getLuminousRelease = api.getLuminousScansReleased(title, url_basic, url_chapter, int(r), int(g),
                                                                          int(b), id_channel,
                                                                          id_guild)
                            if announced.keys().__contains__(f'{id_guild}-{title}'):
                                if float(announced.get(f'{id_guild}-{title}')) < getLuminousRelease[3]:
                                    # I will check the dm_ping file and see if they want dm
                                    dm_subs = []
                                    dm_other = []
                                    subscription_p = getLuminousRelease[2].copy()
                                    subscription = getLuminousRelease[2].copy()
                                    with open('dm_ping', 'r') as r_dm:
                                        for line_dm in r_dm:
                                            split_dm = line_dm.split('-')
                                            guild_dm = split_dm[0]
                                            subs_dm = split_dm[1].split(',')
                                            if str(guild_dm) == str(id_guild):
                                                for s in subs_dm:
                                                    n = s.replace("['", '').replace("']", '')
                                                    dm_subs.append(n)
                                                    if subscription_p.__contains__(n):
                                                        subscription_p.remove(n)
                                            else:
                                                dm_other.append(line_dm)

                                    # -------
                                    channel = bot.get_channel(int(id_channel))
                                    embed = getLuminousRelease[1]
                                    try:
                                        await channel.send(embed=embed)
                                    except:
                                        embed.set_image(url='')
                                        await channel.send(embed=embed)
                                    await channel.send(
                                        f'>>> Ping of The {title} {getLuminousRelease[3]}: {subscription_p}',
                                        delete_after=300)
                                    announced[f'{id_guild}-{title}'] = float(getLuminousRelease[3])
                                    print('------------------------------------')
                                    await channel_print.send('------------------------------------')
                                    print(f'{title} {getLuminousRelease[3]}: {getLuminousRelease[2]}')
                                    await channel_print.send(
                                        str(f'{title} {getLuminousRelease[3]}: {getLuminousRelease[2]}').replace('@',
                                                                                                                 ''))
                                    print('------------------------------------')
                                    await channel_print.send('------------------------------------')

                                    # DM to the user
                                    chapter_num = getLuminousRelease[3]
                                    server = bot.get_guild(int(id_guild))
                                    embed_user = discord.Embed(title=f"{title}", url=f"{url_basic}",
                                                               description=f"The Chapter {chapter_num} was released! \n"
                                                                           f" Link to the chapter: {url_chapter}{int(chapter_num)} \n"
                                                                           f" Server: {server}",
                                                               color=discord.Color.from_rgb(int(r), int(g), int(b)))

                                    # Now I have the dm sub ids
                                    subscription = getLuminousRelease[2]

                                    for sub in subscription:

                                        if dm_subs.__contains__(sub):
                                            id = int(sub.replace('<@', '').replace('>', ''))
                                            user = await bot.fetch_user(id)
                                            await user.send(embed=embed_user)
                                    # --------------
                            else:
                                channel = bot.get_channel(int(id_channel))
                                embed = getLuminousRelease[1]
                                try:
                                    await channel.send(embed=embed)
                                except:
                                    embed.set_image(url='')
                                    await channel.send(embed=embed)
                                await channel.send(
                                    f'>>> Ping of The {title} {getLuminousRelease[3]}: {getLuminousRelease[2]}',
                                    delete_after=300)
                                announced.setdefault(f'{id_guild}-{title}', float(getLuminousRelease[3]))
                                print('------------------------------------')
                                await channel_print.send('------------------------------------')
                                print(f'{title} {getLuminousRelease[3]}: {getLuminousRelease[2]}')
                                await channel_print.send(
                                    str(f'{title} {getLuminousRelease[3]}: {getLuminousRelease[2]}').replace('@', ''))
                                print('------------------------------------')
                                await channel_print.send('------------------------------------')
                        elif source == "MangaKakalot":
                            getMangaKakalotRelease = api.getMangaKakalotReleased(title, url_basic, url_chapter, int(r),
                                                                             int(g),
                                                                             int(b), id_channel,
                                                                             id_guild)
                            if announced.keys().__contains__(f'{id_guild}-{title}'):
                                if float(announced.get(f'{id_guild}-{title}')) < getMangaKakalotRelease[3]:
                                    # I will check the dm_ping file and see if they want dm
                                    dm_subs = []
                                    dm_other = []
                                    subscription_p = getMangaKakalotRelease[2].copy()
                                    subscription = getMangaKakalotRelease[2].copy()
                                    with open('dm_ping', 'r') as r_dm:
                                        for line_dm in r_dm:
                                            split_dm = line_dm.split('-')
                                            guild_dm = split_dm[0]
                                            subs_dm = split_dm[1].split(',')
                                            if str(guild_dm) == str(id_guild):
                                                for s in subs_dm:
                                                    n = s.replace("['", '').replace("']", '')
                                                    dm_subs.append(n)
                                                    if subscription_p.__contains__(n):
                                                        subscription_p.remove(n)
                                            else:
                                                dm_other.append(line_dm)

                                    # -------

                                    channel = bot.get_channel(int(id_channel))
                                    embed = getMangaKakalotRelease[1]
                                    try:
                                        await channel.send(embed=embed)
                                    except:
                                        embed.set_image(url='')
                                        await channel.send(embed=embed)
                                    await channel.send(
                                        f'>>> Ping of The {title} {getMangaKakalotRelease[3]}: {subscription_p}',
                                        delete_after=300)
                                    announced[f'{id_guild}-{title}'] = float(getMangaKakalotRelease[3])
                                    print('------------------------------------')
                                    await channel_print.send('------------------------------------')
                                    print(f'{title} {getMangaKakalotRelease[3]}: {getMangaKakalotRelease[2]}')
                                    await channel_print.send(
                                        str(f'{title} {getMangaKakalotRelease[3]}: {getMangaKakalotRelease[2]}').replace(
                                            '@', ''))
                                    print('------------------------------------')
                                    await channel_print.send('------------------------------------')

                                    # DM to the user
                                    chapter_num = getMangaKakalotRelease[3]
                                    server = bot.get_guild(int(id_guild))
                                    embed_user = discord.Embed(title=f"{title}", url=f"{url_basic}",
                                                               description=f"The Chapter {chapter_num} was released! \n"
                                                                           f" Link to the chapter: {url_chapter}{int(chapter_num)} \n"
                                                                           f" Server: {server}",
                                                               color=discord.Color.from_rgb(int(r), int(g), int(b)))

                                    # Now I have the dm sub ids
                                    subscription = getMangaKakalotRelease[2]

                                    for sub in subscription:
                                        if dm_subs.__contains__(sub):
                                            id = int(sub.replace('<@', '').replace('>', ''))
                                            user = await bot.fetch_user(id)
                                            await user.send(embed=embed_user)
                                    # --------------

                            else:
                                channel = bot.get_channel(int(id_channel))
                                embed = getMangaKakalotRelease[1]
                                try:
                                    await channel.send(embed=embed)
                                except:
                                    embed.set_image(url='')
                                    await channel.send(embed=embed)
                                await channel.send(
                                    f'>>> Ping of The {title} {getMangaKakalotRelease[3]}: {getMangaKakalotRelease[2]}',
                                    delete_after=300)
                                announced.setdefault(f'{id_guild}-{title}', float(getMangaKakalotRelease[3]))
                                print('------------------------------------')
                                await channel_print.send('------------------------------------')
                                print(f'{title} {getMangaKakalotRelease[3]}: {getMangaKakalotRelease[2]}')
                                await channel_print.send(
                                    str(f'{title} {getMangaKakalotRelease[3]}: {getMangaKakalotRelease[2]}').replace(
                                        '@', ''))
                                print('------------------------------------')
                                await channel_print.send('------------------------------------')
                    except Exception as e:
                        print(f'Error of {title}: {e}')
                        await channel_print.send(f'Error of {title}: {e}')
        print(announced)
        await channel_print.send(announced)
        end = datetime.now().strftime('%H:%M:%S')
        print(f'Refreshing releases status: Finished {end}')
        await channel_print.send(f'Refreshing releases status: Finished {end}')
    except Exception as e:
        end = datetime.now().strftime('%H:%M:%S')
        print(f'Couldn´t refresh the releases {end}')
        await channel_print.send(f'Couldnt refresh the releases {end}')
        print(f'Error: {e}')
        await channel_print.send(f'Error: {str(e)}')
    return announced


