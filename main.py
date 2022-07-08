from discord.ext import tasks
import discord
from discord.ext import commands
import os
import sys
import release
import apis as api
import callables as call
from colorthief import ColorThief
from PIL import Image

bot = commands.Bot(command_prefix="!")

# await bot.wait_until_ready()
print("DokjaBot activated")

img = Image.open("archmage.jpg")

announced = {}

'''with open('server_latest', 'r') as r_an:
    for line in r_an:
        if line != ('' or ' '):
            split = line.split('-')
            announced.setdefault(f'{split[0]}-{split[1]}', float(split[2]))
print(announced)'''


@tasks.loop(seconds=60)
async def rich_presence():
    await bot.wait_until_ready()
    guilds = bot.guilds
    number_of_servers = len(guilds)
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(f'Library of Culture on {number_of_servers} servers'), )


@bot.command()
async def m(ctx, *args):
    cmds = []
    manhwas = []
    try:
        id_channel = ctx.message.channel.id
        id_guild = ctx.message.guild.id
    except:
        id_guild = 0
        id_channel = 0
    with open('channel_listed', 'r', errors='ignore') as r:
        for line in r:
            if line is not None:
                id_line = (line.split("  ")[0])
                if str(id_line) == str(id_guild):
                    manhwas.append(line)
    for line in manhwas:
        line = line.split("  ")
        cmds.append(line[2])

    '''if cmds.__contains__(args[0]):
        # Now look into chapters and find it
        with open("channel_listed", "r") as read_cl:
            for line_cl in read_cl:
                line_cl_split = line_cl.split("  ")'''

    '''for manhwa in manhwas:
            manhwa = manhwa.split("  ")
            if manhwa[2] == args[0]:
                # Now we found the manhwa we wanted
                source = manhwa[4].replace(" ", "")
                if source == 'ReaperScans':
                    embed = \
                        api.getReaperScans(manhwa[3], manhwa[5], manhwa[6], int(manhwa[7]), int(manhwa[8]),
                                           int(manhwa[9]),
                                           int(manhwa[10]), int(manhwa[11]), int(manhwa[12]), str(id_guild))[0]
                    await ctx.send(embed=embed)
                elif source == 'MangaClash':
                    embed = \
                        api.getMangaClash(manhwa[3], manhwa[5], manhwa[6], int(manhwa[7]), int(manhwa[8]),
                                          int(manhwa[9]),
                                          int(manhwa[10]), int(manhwa[11]), int(manhwa[12]), str(id_guild))[0]
                    await ctx.send(embed=embed)
                elif source == 'LuminousScans':
                    embed = \
                        api.getLuminousScans(manhwa[3], manhwa[5], manhwa[6], int(manhwa[7]), int(manhwa[8]),
                                             int(manhwa[9]),
                                             int(manhwa[10]), int(manhwa[11]), int(manhwa[12]), str(id_guild))[0]
                    await ctx.send(embed=embed)
                elif source == 'MangaKakalot':
                    embed = \
                        api.getMangaKakalot(manhwa[3], manhwa[5], manhwa[6], int(manhwa[7]), int(manhwa[8]),
                                            int(manhwa[9]),
                                            int(manhwa[10]), int(manhwa[11]), int(manhwa[12]), str(id_guild))[0]
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("We don't support this source")'''
    if args[0] == "list":
        release_list = "\n"
        with open("channel_listed","r") as read_cl:
            for line_cl in read_cl:
                line_cl = line_cl.split("  ")
                guild_ids = line_cl[0].replace("[","").replace(" ","").replace("]","").replace("'","").split(",")
                print(guild_ids)
                print(id_guild)
                if guild_ids.__contains__(str(id_guild)):
                    release_list += f"{line_cl[3]}: !m {line_cl[2]}\n"
        embed = discord.Embed(title=f"List of Manhwas/Mangas",
                              description=f"The list of commands for \n " + "Manhwas and Mangas in system" + f"\n {release_list}",
                              color=discord.Color.from_rgb(246, 214, 4))
        await ctx.send(embed=embed)
    elif args[0] == "test":
        '''embed = getMangaClashReleased("The Beginning After The End","https://mangaclash.com/manga/the-beginning-after-the-end/","https://mangaclash.com/manga/the-beginning-after-the-end/chapter-", 0,0,0)[0]
        await ctx.send(embed = embed)'''

    elif args[0] == "help":
        embed = discord.Embed(title=f"DokjaBot - Help Menu",
                              description=f'The list of commands for DokjaBot \n'
                                          f'!m list - writes down every manga/manhwa in the server library \n'
                                          f'!m library add <Source> <Title> \n'
                                          f'  - source, you can see all the sources possible by writing !m sources \n'
                                          f'  -  Title, has to be exactly the same as the name from'
                                          f'     the source u specified\n'
                                          f'example: !m library add ReaperScans The World After the Fall\n'
                                          f'!m library sub <title> and !m library unsub <title> \n'
                                          f'  - if you dont know the title, find it in !m list',
                              color=discord.Color.from_rgb(246, 214, 4))
        await ctx.send(embed=embed)
    elif args[0] == "sources":
        embed = discord.Embed(title=f"DokjaBot - Sources",
                              description=f'When asked for source, write the code of source'
                                          f'The sources we support are \n'
                                          f'----Name----------Code----\n'
                                          f'Reaper Scans: ReaperScans \n'
                                          f'MangaClash: MangaClash \n'
                                          f'Luminous Scans: LuminousScans \n'
                                          f'MangaKakalot: MangaKakalot',
                              color=discord.Color.from_rgb(246, 214, 4))
        await ctx.send(embed=embed)
    elif args[0] == "library":
        if args[1] == "add":
            if args[2] == "MangaClash" or args[2] =="ReaperScans" or args[2] =="MangaKakalot" or args[2] =="LuminousScans":
                searched_title = ""
                # for every arg from the 3th to the last one
                for i in range(len(args) - 3):
                    searched_title += f"{args[i + 3]} "
                search = False
                searched_title = searched_title[:len(searched_title) - 1].replace("–", "-")
                if args[2] == "ReaperScans":
                    search = api.searchReaperScans(searched_title)
                    source = "ReaperScans"
                elif args[2] == "MangaClash":
                    search = api.searchMangaClash(searched_title)
                    source = "MangaClash"
                elif args[2] == "MangaKakalot":
                    search = api.searchReaperScans(searched_title)
                    source = "MangaKakalot"
                elif args[2] == "LuminousScans":
                    search = api.searchReaperScans(searched_title)
                    source = "LuminousScans"
                if search[0] is True and search[7] is False:
                    # tell it was found but was a novel
                    embed = discord.Embed(title=f"Search of {searched_title}",
                                          description=f"- Found \n "
                                                      f"- A Novel \n"
                                                      f"= Not added \n"
                                                      f"+ Try adding: -Manhwa",
                                          color=discord.Color.from_rgb(255, 255, 0))
                    await ctx.send(embed=embed, delete_after=60)
                elif search[0] is False:
                    # tell it wasnt found
                    embed = discord.Embed(title=f"Search of {searched_title}",
                                          description=f"- Not Found \n ",
                                          color=discord.Color.from_rgb(255, 0, 0))
                    await ctx.send(embed=embed, delete_after=60)
                else:
                    # found
                    url = search[1]
                    title = search[2]
                    r = search[3]
                    g = search[4]
                    b = search[5]
                    cmd = search[6]
                    # if it returns as False it wasnt added already, but if its true, its already in libraryy
                    am = call.add_manga(str(id_guild), str(id_channel), cmd, searched_title, source, url, r, g, b)
                    if am is False:
                        embed = discord.Embed(title=f"Search of {searched_title}",
                                              description=f"- Found \n "
                                                          f"- Added to library \n "
                                                          f"- cmd: {cmd}",
                                              color=discord.Color.from_rgb(0, 255, 0))
                        await ctx.send(embed=embed, delete_after=60)
                    else:
                        embed = discord.Embed(title=f"Search of {searched_title}",
                                              description=f"- Found \n "
                                                          f"- Already in library \n "
                                                          f"- cmd: {cmd}",
                                              color=discord.Color.from_rgb(255, 255, 0))
                        await ctx.send(embed=embed, delete_after=60)
            else:
                await ctx.send(f">>> You didn't specify the source! \n"
                               f"Example: !m library search add ReaperScans Title")
        elif args[1] == "remove":
            #      0       1           2
            # !m library remove Archmage Streamer
            content_cl = []
            content_sl = []
            content_rsl = []
            cmds = []
            found = False
            searched_title = ""
            others = False
            # for every arg from the 2th to the last one
            for i in range(len(args) - 2):
                if i != (len(args) -3):
                    searched_title += f"{args[i + 2]} "
                else:
                    searched_title += f"{args[i + 2]}"
            # I will copy every line
            with open('channel_listed', 'r', errors='ignore') as r_cl:
                for line_cl in r_cl:
                    if line_cl != ' \n' and line_cl != '':
                        # Make sure theer will be no empty lines
                        line_ = line_cl.split("  ")
                        guild_ids = line_[0].replace("[","").replace(" ","").replace("]","").replace("'","").split(",")
                        if guild_ids.__contains__(str(id_guild)):
                            # it is the cmd from the server
                            title = f'{line_[3]}'
                            if str(title) == str(searched_title):
                                # It is the manga we want to remove from server library
                                found = True
                                channel_ids = line_[0].replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
                                index = guild_ids.index(str(id_guild))
                                guild_ids.remove(str(id_guild))
                                channel_ids.remove(channel_ids[index])
                                # Checkin if there is more servers using this book
                                # if yes, I have to write it down back, but if not, its useless there
                                print(guild_ids)
                                if len(guild_ids) > 0:
                                    others = True
                                    content_cl.append(f"{guild_ids}  {channel_ids}  {line_[2]}  {line_[3]}  {line_[4]}  {line_[5]}  {line_[6]}  {line_[7]}  {line_[8]}")
                            else:
                                content_cl.append(line_cl)
                        else:
                            content_cl.append(line_cl)
            if found is True:
                # I need to delete it from server_latest
                if others is False:
                    with open('server_latest', 'r', errors='ignore') as r_sl:
                        for line_sl in r_sl:
                            if line_sl != ' \n' or line_sl != '':
                                # Make sure theer will be no empty lines
                                line_ = line_sl.split("-+-")
                                title_ = f'{line_[1]}'
                                if title_ == str(searched_title):
                                    # it is the cmd from the server
                                    if str(title) != str(title_):
                                        content_sl.append(line_sl)
                                else:
                                    content_sl.append(line_sl)
                    # I need to delete it from server_release_ping
                    #Now I need to rewrite server_latest
                    with open('server_latest', 'w', errors='ignore') as w_sl:
                        for item in content_sl:
                            if not item.__contains__("\n"):
                                item += ' \n'
                            w_sl.write(item)
                with open('server_release_ping', 'r', errors='ignore') as r_srp:
                    for line_srp in r_srp:
                        if line_srp != ' \n' and line_srp != '':
                            line_split = line_srp.split('-+-')
                            if id_guild == int(line_split[0]):
                                # Its the same server
                                title_ = f'{line_split[1]}'
                                if str(searched_title) != str(title_):
                                    content_rsl.append(line_srp)
                            else:
                                content_rsl.append(line_srp)
                # Now I just rewrite it to server_release_ping
                with open('server_release_ping', 'w', errors='ignore') as w_srp:
                    for lin in content_rsl:
                        if not lin.__contains__("\n"):
                            lin += ' \n'
                        w_srp.write(lin)

                # Now I need to rewrite the channel_listed
                with open('channel_listed', 'w', errors='ignore') as w_cl:
                    for c in content_cl:
                        if not c.__contains__("\n"):
                            c += ' \n'
                        w_cl.write(c)



                await ctx.send(f'>>> The book in library with Title: {searched_title} has been removed!')
            else:
                await ctx.send(f'>>> The book in library with Title: {searched_title} was **not** found!')
        elif args[1] == "sub":
            poss_subs = []
            subscriptions = []
            subscriptions_other = []
            found = False
            already_in = False
            with open('server_release_ping', 'r') as read:
                for line in read:
                    line_s = line.split('-+-')
                    if line_s[0] == str(id_guild):
                        # It is one of the servers pings

                        # I need to make a title so
                        title = ''
                        count = 0
                        max = len(args) - 1
                        for arg in args:
                            if count >= 2 and count != max:
                                title += f'{arg} '
                            elif count == max:
                                title += arg
                            count += 1
                        if line_s[1] == title:
                            found = True
                            # Its the same title so now just get the users already in lsit and add the new one
                            # , but check if he isnt there already
                            users = line_s[2].replace("[", "").replace("]", "").replace("'", '').replace("\\n", '').replace("\n", '').replace(" ", '').replace("  ", '').split(",")
                            if users.__contains__(ctx.author.mention):
                                await ctx.send('>>> You have already subscribed to updates from this manhwa/manga')
                                already_in = True
                            else:
                                users.append(f'{ctx.author.mention}')
                                for item in users:
                                    if item == '' or item == '\n' or item == ' ':
                                        users.remove(item)
                                subscriptions.append(f'{id_guild}-+-{title}-+-{users}')
                        else:
                            subscriptions_other.append(line)
                    else:
                        subscriptions_other.append(line)
                if found and not already_in:
                    await ctx.send(f'>>> You have subscribed to the {title}')
                if not already_in and found:
                    with open('server_release_ping', 'w') as w_srp:
                        for subs in subscriptions:
                            w_srp.write(f'{subs} \n')
                        for subs in subscriptions_other:
                            w_srp.write(subs)
            if not found:
                await ctx.send('>>> Coulnd´t find the desired manhwa/manga \nTry check the title again')
        elif args[1] == "unsub":
            subscription_searched = []
            subscription_other = []
            found = False
            contain = False
            # I need to get the title
            title = ''
            count = 0
            max = len(args) - 1
            for arg in args:
                if count >= 2 and count != max:
                    title += f'{arg} '
                elif count == max:
                    title += arg
                count += 1
            # Now I can read the file and edit it accordingly

            with open('server_release_ping', 'r') as read:
                for line in read:
                    if line != ('' or ' '):
                        splited = line.split('-+-')
                        if splited[0] == str(id_guild):
                            # Its the correct server
                            if title == splited[1]:
                                # Its the correct title
                                found = True
                                # Its the same title so now just get the users already in lsit and add the new one
                                # , but check if he isnt there already
                                users = splited[2].replace("[", "")
                                users = users.replace("]", "")
                                users = users.replace("'", '')
                                users = users.replace("\\n", '')
                                users = users.replace("\n", '')
                                users = users.replace(" ", '')
                                users = users.replace("  ", '')
                                users = users.split(",")

                                if users.__contains__(str(ctx.author.mention)):
                                    # It does contain user
                                    contain = True
                                    users.remove(str(ctx.author.mention))
                                    subscription_searched.append(f'{id_guild}-+-{title}-+-{users}')
                            else:
                                subscription_other.append(line)
                        else:
                            subscription_other.append(line)
                    with open('server_release_ping', 'w') as write:
                        for subs in subscription_searched:
                            write.write(f'{subs} \n')
                        for subs in subscription_other:
                            write.write(subs)
                new = True
            if found and contain:
                await ctx.send(f'>>> You have unsubscribed the {title}')
            elif found and not contain:
                await ctx.send(f'>>> You haven´t been subscribed to the {title}')
            else:
                await ctx.send(f'>>> The {title} was not found \n Check if you wrote title correctly')
    elif args[0] == "dm":
        dm_ping = []
        dm_other = []
        with open('dm_ping', 'r') as r_dm:
            for line in r_dm:
                split_dm = line.split('-+-')
                if split_dm[0] == str(id_guild):
                    dm_list = split_dm[1].replace("['", '').replace("']", '').replace("'", '').replace(' ', '').split(
                        ',')
                    for s in dm_list:
                        s.replace(' ', '')
                        if s != '[]':
                            dm_ping.append(s)
                else:
                    dm_other.append(line)
        if dm_ping.__contains__(ctx.author.mention):
            dm_ping.remove(ctx.author.mention)
            await ctx.send('>>> You have disabled DirectMessages for this server!')
        else:
            dm_ping.append(ctx.author.mention)
            await ctx.send('>>> You have enabled DirectMessages for this server!')

        # Now I will save it to the file
        with open('dm_ping', 'w') as w_dm:
            w_dm.write(f'{id_guild}-+-{dm_ping} \n')
            for p in dm_other:
                w_dm.write(p)
    else:
        await ctx.send('>>> Unknown command!')


First = True


def getF(f):
    return f


def setF():
    global First
    First = False


def getAnnounced(a):
    return a


def setAnnounced(release_check):
    global announced
    announced = release_check


@tasks.loop(minutes=60)
async def periodical_restart():
    await bot.wait_until_ready()
    is_first = getF(First)
    print(f'Is it the first: {is_first}')
    if not is_first:
        os.execl(sys.executable, sys.executable, *sys.argv)
        print('restarted')
    else:
        setF()
        print('Set False')


@tasks.loop(seconds=60)
async def releaseCheck():
    release_check = await release.chapterreleasecheck(bot, announced)
    #setAnnounced(release_check)


# <@401845652541145089>
# periodical_restart.start()
releaseCheck.start()
# rich_presence.start()
bot.run('')
