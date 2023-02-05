from nextcord.ext import tasks
from nextcord.ext import commands
from nextcord import Interaction
import nextcord

# from nextcord.ext import Interaction
import os
import sys
import release
import apis as api
import callables as call



intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
client = nextcord.Client(intents=intents)
serverID = []
@tasks.loop(seconds=60)
async def setGuilds():
    serverID = []
    await bot.wait_until_ready()
    for guild in bot.guilds:
        serverID.append(int(guild.id))
    print(f"server ids {serverID}")




#serverID = 855860264942829589


@bot.slash_command(name="ping", description="Check bots ping!", guild_ids=serverID)
async def pingtest(interaction: Interaction):
    await interaction.response.send_message(f"My ping is Idk how many/ms")


# await bot.wait_until_ready()
print("DokjaBot activated - Made by DioForever - dioforever.live")

announced = {}


@tasks.loop(seconds=60)
async def rich_presence():
    await bot.wait_until_ready()
    guilds = bot.guilds
    number_of_servers = len(guilds)
    await bot.change_presence(status=nextcord.Status.online,
                              activity=nextcord.Game(f'Library of Culture on {number_of_servers} servers'), )

@bot.slash_command(name="library_addrole", description="Adds role ping to specific manga/manhwa.", guild_ids=serverID)
@commands.has_permissions(administrator=True)
async def library_add(interaction: Interaction, role: str, title: str):
    print(role)
    await interaction.response.send_message(role)

@bot.slash_command(name="library_add", description="Adds the manga to the server library", guild_ids=serverID)
async def library_add(interaction: Interaction, source: str, title_or_url: str):
    if Interaction.message.author.guild_permissions.administrator:
        if source == "MangaClash" or source == "ReaperScans" or source == "MangaKakalot" or source == "LuminousScans":
            try:
                id_channel = interaction.channel_id
                id_guild = interaction.guild_id
            except:
                id_guild = None
                id_channel = None
            search = False

            searched_title = title_or_url.replace("–", "-")
            if source == "ReaperScans":
                search = api.searchReaperScans(searched_title)
                source = "ReaperScans"
            elif source == "MangaClash":
                search = api.searchMangaClash(searched_title)
                source = "MangaClash"
            elif source == "MangaKakalot":
                search = api.searchMangaKakalot(searched_title)
                source = "MangaKakalot"
            elif source == "LuminousScans":
                search = api.searchLuminousScans(searched_title)
                source = "LuminousScans"
            error = search[8]
            if error is False:
                if search[0] is True and search[7] is False:
                    # tell it was found but was a novel
                    embed = nextcord.Embed(title=f"Search of {searched_title}",
                                           description=f"- Found \n "
                                                       f"- A Novel \n"
                                                       f"= Not added \n"
                                                       f"+ Try adding: -Manhwa",
                                           color=nextcord.Color.from_rgb(255, 255, 0))
                    await interaction.response.send_message(embed=embed)
                elif search[0] is False:
                    # tell it wasnt found
                    embed = nextcord.Embed(title=f"Search of {searched_title}",
                                           description=f"- Not Found \n ",
                                           color=nextcord.Color.from_rgb(255, 0, 0))
                    await interaction.response.send_message(embed=embed)
                else:
                    # found
                    url = search[1]
                    title = search[2]
                    r = search[3]
                    g = search[4]
                    b = search[5]
                    cmd = search[6]
                    # if it returns as False it wasnt added already, but if its true, its already in libraryy
                    am = call.add_manga(str(id_guild), str(id_channel), cmd, title, source, url, r, g, b)
                    if am is False:
                        embed = nextcord.Embed(title=f"Search of {title}",
                                               description=f"- Found \n "
                                                           f"- Added to library \n "
                                                           f"- cmd: {cmd} \n"
                                                           f"- url: {url}",
                                               color=nextcord.Color.from_rgb(0, 255, 0))
                        await interaction.response.send_message(embed=embed)
                    else:
                        embed = nextcord.Embed(title=f"Search of {title}",
                                               description=f"- Found \n "
                                                           f"- Already in library \n "
                                                           f"- cmd: {cmd}",
                                               color=nextcord.Color.from_rgb(255, 255, 0))
                        await interaction.response.send_message(embed=embed)
            else:
                embed = nextcord.Embed(title=f"Search of {searched_title}",
                                       description=f"- Not Found \n "
                                                   f"- If error appeared their  \n"
                                                   f"- website may be down \n"
                                                   f"- try check their website or \n"
                                                   f"- correct the searched title \n"
                                                   f"+ you can use a link as well ",
                                       color=nextcord.Color.from_rgb(255, 0, 0))
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f">>> You didn't specify the source! \n"
                           f"Example: !m library search add ReaperScans Title")
    else:
        await interaction.response.send_message(f">>> You dont have permission to this command!", delete_after=5)

        #await interaction.response.send_message(f"Added to library {title_or_url} from {source}")

@bot.slash_command(name="library_remove", description="Removes the manga from the server library", guild_ids=serverID)
async def library_remove(interaction: Interaction, source: str, title: str):
    try:
        id_guild = interaction.guild_id
    except:
        id_guild = None
    #      0       1           2
    # !m library remove Archmage Streamer
    if Interaction.message.author.guild_permissions.administrator:
        id_guild = str(id_guild)
        content_cl = []
        content_sl = []
        content_rsl = []
        cmds = []
        found = False
        searched_title = ""
        others = False
        # bool, I need to know if there is some other book with  the same title which means has same server_release_ping
        same_title = False
        # I will copy every line
        searched_title = title
        with open('channel_listed', 'r', errors='ignore') as r_cl:
            for line_cl in r_cl:
                if line_cl != ' \n' and line_cl != '':
                    # Make sure there will be no empty lines
                    line_ = line_cl.split("  ")
                    guild_ids = line_[0].replace("[", "").replace(" ", "").replace("]", "").replace("'", "").split(
                        ",")
                    print(guild_ids, id_guild)
                    # it is the cmd from the server
                    title = f'{line_[3]}'
                    print(title, searched_title)
                    print(line_[4], source)
                    if guild_ids.__contains__(str(id_guild)):
                        # it is the cmd from the server
                        if str(title) == str(searched_title) and line_[4] == source:
                            # It is the manga we want to remove from server library
                            found = True
                            channel_ids = line_[0].replace("[", "").replace("]", "").replace(" ", "").replace("'",
                                                                                                              "").split(
                                ",")
                            index = guild_ids.index(str(id_guild))
                            guild_ids.remove(str(id_guild))
                            channel_ids.remove(channel_ids[index])
                            # Checkin if there is more servers using this book
                            # if yes, I have to write it down back, but if not, its useless there
                            if len(guild_ids) > 0:
                                others = True
                                content_cl.append(
                                    f"{guild_ids}  {channel_ids}  {line_[2]}  {line_[3]}  {line_[4]}  {line_[5]}  {line_[6]}  {line_[7]}  {line_[8]}")
                        else:
                            content_cl.append(line_cl)
                    else:
                        content_cl.append(line_cl)
                    if guild_ids.__contains__(id_guild) and title == searched_title:
                        same_title = True
        if found is True:
            # I need to delete it from server_latest
            if others is False:
                with open('server_latest', 'r', errors='ignore') as r_sl:
                    for line_sl in r_sl:
                        if line_sl != ' \n' or line_sl != '':
                            # Make sure theer will be no empty lines
                            line_ = line_sl.split("-+-")
                            title_ = f'{line_[1]}'
                            if line_[0] == str(source):
                                if title_ != str(searched_title):
                                    content_sl.append(line_sl)
                            else:
                                content_sl.append(line_sl)
                # I need to delete it from server_release_ping
                # Now I need to rewrite server_latest
                with open('server_latest', 'w', errors='ignore') as w_sl:
                    for item in content_sl:
                        if not item.__contains__("\n"):
                            item += ' \n'
                        w_sl.write(item)
            if same_title is False:
                with open('server_release_ping', 'r', errors='ignore') as r_srp:
                    for line_srp in r_srp:
                        if line_srp != ' \n' and line_srp != '':
                            line_split = line_srp.split('-+-')
                            if str(id_guild) == str(line_split[0]):
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

            await interaction.response.send_message(f'>>> The book in library with Title: {searched_title} has been removed!', delete_after=5)
        else:
            await interaction.response.send_message(f'>>> The book in library with Title: {searched_title} was **not** found!', delete_after=5)
    else:
        await interaction.response.send_message(f">>> You dont have permission to this command!", delete_after=5)

@bot.slash_command(name="dm", description="Enables/Disables direct messages instead of pings from this server announcements.", guild_ids=serverID)
async def dm_enable_disable(interaction: Interaction):
    try:
        id_guild = interaction.guild_id
    except:
        id_guild = None
    dm_other = []
    with open('dm_ping', 'r') as r_dm:
        for line in r_dm:
            split_dm = line.split('-+-')
            if split_dm[0] == str(id_guild):
                dm_list = split_dm[1].replace("['", '').replace("']", '').replace("\n", '').replace("'",'').replace(' ','').split(',')
                if dm_list.__contains__("[]"):
                    dm_list.remove("[]")
            else:
                dm_other.append(line)
    if dm_list.__contains__(interaction.user.mention):
        dm_list.remove(interaction.user.mention)
        embed = nextcord.Embed(title=f"DirectMessages",
                               description=f"You have disabled DirectMessages!",
                               color=nextcord.Color.from_rgb(255, 0, 0))
        await interaction.response.send_message(embed=embed)
    else:
        dm_list.append(interaction.user.mention)
        embed = nextcord.Embed(title=f"DirectMessages",
                               description=f"You have enabled DirectMessages!",
                               color=nextcord.Color.from_rgb(0, 255, 0))
        await interaction.response.send_message(embed=embed)

    # Now I will save it to the file
    with open('dm_ping', 'w') as w_dm:
        w_dm.write(f'{id_guild}-+-{dm_list} \n')
        for p in dm_other:
            w_dm.write(p)

@bot.slash_command(name="sub", description="Subscribe to any book in the library of the server.", guild_ids=serverID)
async def sub(interaction: Interaction, title: str):
    try:
        id_guild = interaction.guild_id
    except:
        id_guild = None
    subscriptions = []
    subscriptions_other = []
    found = False
    already_in = False
    with open('server_release_ping', 'r') as read:
        for line in read:
            line_s = line.split('-+-')
            if line_s[0] == str(id_guild):
                # It is one of the servers pings

                if line_s[1] == title:
                    found = True
                    # Its the same title so now just get the users already in lsit and add the new one
                    # , but check if he isnt there already
                    users = line_s[2].replace("[", "").replace("]", "").replace("'", '').replace("\\n",
                                                                                                 '').replace(
                        "\n", '').replace(" ", '').replace("  ", '').split(",")
                    if users.__contains__(interaction.user.mention):
                        await interaction.response.send_message('>>> You have already subscribed to updates from this manhwa/manga')
                        already_in = True
                    else:
                        users.append(f'{interaction.user.mention}')
                        for item in users:
                            if item == '' or item == '\n' or item == ' ':
                                users.remove(item)
                        subscriptions.append(f'{id_guild}-+-{title}-+-{users}')
                else:
                    subscriptions_other.append(line)
            else:
                subscriptions_other.append(line)
        if found and not already_in:
            await interaction.response.send_message(f'>>> You have subscribed to the {title}', delete_after=5)
        if not already_in and found:
            with open('server_release_ping', 'w') as w_srp:
                for subs in subscriptions:
                    w_srp.write(f'{subs} \n')
                for subs in subscriptions_other:
                    w_srp.write(subs)
    if not found:
        await interaction.response.send_message('>>> Coulnd´t find the desired manhwa/manga \nTry check the title again', delete_after=5)

@bot.slash_command(name="unsub", description="Unsubscribe any book in the library of the server.", guild_ids=serverID)
async def unsub(interaction: Interaction, title: str):
    try:
        id_guild = interaction.guild_id
    except:
        id_guild = None
    if id_guild is not None:
        subscription_searched = []
        subscription_other = []
        found = False
        contain = False
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

                            if users.__contains__(str(interaction.message.author.mention)):
                                # It does contain user
                                contain = True
                                users.remove(str(interaction.message.author.mention))
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
            await interaction.response.send_message(f'>>> You have unsubscribed the {title}', delete_after=5)
        elif found and not contain:
            await interaction.response.send_message(f'>>> You haven´t been subscribed to the {title}', delete_after=5)
        else:
            await interaction.response.send_message(f'>>> The {title} was not found \n Check if you wrote title correctly', delete_after=5)

@bot.slash_command(name="sources", description="See all the available sources.", guild_ids=serverID)
async def sources(interaction: Interaction):
    embed = nextcord.Embed(title=f"DokjaBot - Sources",
                           description=f'When asked for source, write the code of source'
                                       f'The sources we support are \n'
                                       f'----Name----------Code----\n'
                                       f'Reaper Scans: ReaperScans \n'
                                       f'MangaClash: MangaClash \n'
                                       f'Luminous Scans: LuminousScans \n'
                                       f'MangaKakalot: MangaKakalot',
                           color=nextcord.Color.from_rgb(246, 214, 4))
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="help", description="Need help?", guild_ids=serverID)
async def help(interaction: Interaction):
    embed = nextcord.Embed(title=f"DokjaBot - Help Menu",
                           description=f'The list of commands for DokjaBot \n'
                                       f'!m list - writes down every manga/manhwa in the server library \n'
                                       f'!m library add <Source> <Title> \n'
                                       f'  - source, you can see all the sources possible by writing !m sources \n'
                                       f'  -  Title, has to be exactly the same as the name from'
                                       f'     the source u specified\n'
                                       f'example: !m library add ReaperScans The World After the Fall\n'
                                       f'example: !m library add MangaKakalot https://mangakakalot.com/manga/yn929447\n'
                                       f'!m library sub <title> and !m library unsub <title> \n'
                                       f'  - if you dont know the title, find it in !m list',
                           color=nextcord.Color.from_rgb(246, 214, 4))
    await interaction.response.send_message(embed=embed)
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
    if args[0] == "list":
        release_list = "\n"
        with open("channel_listed", "r") as read_cl:
            for line_cl in read_cl:
                line_cl = line_cl.split("  ")
                guild_ids = line_cl[0].replace("[", "").replace(" ", "").replace("]", "").replace("'", "").split(",")
                if guild_ids.__contains__(str(id_guild)):
                    release_list += f"{line_cl[3]}: !m {line_cl[2]}\n"
        embed = nextcord.Embed(title=f"List of Manhwas/Mangas",
                               description=f"The list of commands for \n " + "Manhwas and Mangas in system" + f"\n {release_list}",
                               color=nextcord.Color.from_rgb(246, 214, 4))
        await ctx.send(embed=embed)
    elif args[0] == "test":
        '''embed = getMangaClashReleased("The Beginning After The End","https://mangaclash.com/manga/the-beginning-after-the-end/","https://mangaclash.com/manga/the-beginning-after-the-end/chapter-", 0,0,0)[0]
        await ctx.send(embed = embed)'''
        embed = nextcord.Embed(title="Title", description="Desc", color=0x00ff00)  # creates embed
        file = nextcord.File("img.png", filename="img.png")
        embed.set_image(url="attachment://img.png")
        await ctx.send(file=file, embed=embed)
    elif args[0] == "help":
        embed = nextcord.Embed(title=f"DokjaBot - Help Menu",
                               description=f'The list of commands for DokjaBot \n'
                                           f'!m list - writes down every manga/manhwa in the server library \n'
                                           f'!m library add <Source> <Title> \n'
                                           f'  - source, you can see all the sources possible by writing !m sources \n'
                                           f'  -  Title, has to be exactly the same as the name from'
                                           f'     the source u specified\n'
                                           f'example: !m library add ReaperScans The World After the Fall\n'
                                           f'example: !m library add MangaKakalot https://mangakakalot.com/manga/yn929447\n'
                                           f'!m library sub <title> and !m library unsub <title> \n'
                                           f'  - if you dont know the title, find it in !m list',
                               color=nextcord.Color.from_rgb(246, 214, 4))
        await ctx.send(embed=embed)
    elif args[0] == "sources":
        embed = nextcord.Embed(title=f"DokjaBot - Sources",
                               description=f'When asked for source, write the code of source'
                                           f'The sources we support are \n'
                                           f'----Name----------Code----\n'
                                           f'Reaper Scans: ReaperScans \n'
                                           f'MangaClash: MangaClash \n'
                                           f'Luminous Scans: LuminousScans \n'
                                           f'MangaKakalot: MangaKakalot',
                               color=nextcord.Color.from_rgb(246, 214, 4))
        await ctx.send(embed=embed)
    elif args[0] == "library":
        if args[1] == "add":
            if args[2] == "MangaClash" or args[2] == "ReaperScans" or args[2] == "MangaKakalot" or args[
                2] == "LuminousScans":
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
                    search = api.searchMangaKakalot(searched_title)
                    source = "MangaKakalot"
                elif args[2] == "LuminousScans":
                    search = api.searchLuminousScans(searched_title)
                    source = "LuminousScans"
                error = search[8]
                if error is False:
                    if search[0] is True and search[7] is False:
                        # tell it was found but was a novel
                        embed = nextcord.Embed(title=f"Search of {searched_title}",
                                               description=f"- Found \n "
                                                           f"- A Novel \n"
                                                           f"= Not added \n"
                                                           f"+ Try adding: -Manhwa",
                                               color=nextcord.Color.from_rgb(255, 255, 0))
                        await ctx.send(embed=embed)
                    elif search[0] is False:
                        # tell it wasnt found
                        embed = nextcord.Embed(title=f"Search of {searched_title}",
                                               description=f"- Not Found \n ",
                                               color=nextcord.Color.from_rgb(255, 0, 0))
                        await ctx.send(embed=embed)
                    else:
                        # found
                        url = search[1]
                        title = search[2]
                        r = search[3]
                        g = search[4]
                        b = search[5]
                        cmd = search[6]
                        # if it returns as False it wasnt added already, but if its true, its already in libraryy
                        am = call.add_manga(str(id_guild), str(id_channel), cmd, title, source, url, r, g, b)
                        if am is False:
                            embed = nextcord.Embed(title=f"Search of {title}",
                                                   description=f"- Found \n "
                                                               f"- Added to library \n "
                                                               f"- cmd: {cmd} \n"
                                                               f"- url: {url}",
                                                   color=nextcord.Color.from_rgb(0, 255, 0))
                            await ctx.send(embed=embed)
                        else:
                            embed = nextcord.Embed(title=f"Search of {title}",
                                                   description=f"- Found \n "
                                                               f"- Already in library \n "
                                                               f"- cmd: {cmd}",
                                                   color=nextcord.Color.from_rgb(255, 255, 0))
                            await ctx.send(embed=embed)
                else:
                    embed = nextcord.Embed(title=f"Search of {searched_title}",
                                           description=f"- Not Found \n "
                                                       f"- If error appeared their  \n"
                                                       f"- website is probably down \n"
                                                       f"- try check their website or \n"
                                                       f"- correct the searched title \n"
                                                       f"+ you can use a link as well ",
                                           color=nextcord.Color.from_rgb(255, 0, 0))
                    await ctx.send(embed=embed)
            else:
                await ctx.send(f">>> You didn't specify the source! \n"
                               f"Example: !m library search add ReaperScans Title")
            # deltes the message sent by user
            # await ctx.message.delete()
        elif args[1] == "remove":
            #      0       1           2
            # !m library remove Archmage Streamer
            id_guild = str(id_guild)
            content_cl = []
            content_sl = []
            content_rsl = []
            cmds = []
            found = False
            searched_title = ""
            others = False
            # for every arg from the 2th to the last one
            source = args[2]
            for i in range(len(args) - 3):
                if i != (len(args) - 3):
                    searched_title += f"{args[i + 3]} "
                else:
                    searched_title += f"{args[i + 3]}"
            # bool, I need to know if there is some other book with  the same title which means has same server_release_ping
            same_title = False
            # I will copy every line
            searched_title = searched_title[:-1]
            with open('channel_listed', 'r', errors='ignore') as r_cl:
                for line_cl in r_cl:
                    if line_cl != ' \n' and line_cl != '':
                        # Make sure theer will be no empty lines
                        line_ = line_cl.split("  ")
                        guild_ids = line_[0].replace("[", "").replace(" ", "").replace("]", "").replace("'", "").split(
                            ",")
                        if guild_ids.__contains__(str(id_guild)):
                            # it is the cmd from the server
                            title = f'{line_[3]}'
                            if str(title) == str(searched_title) and line_[4] == source:
                                # It is the manga we want to remove from server library
                                found = True
                                channel_ids = line_[0].replace("[", "").replace("]", "").replace(" ", "").replace("'",
                                                                                                                  "").split(
                                    ",")
                                index = guild_ids.index(str(id_guild))
                                guild_ids.remove(str(id_guild))
                                channel_ids.remove(channel_ids[index])
                                # Checkin if there is more servers using this book
                                # if yes, I have to write it down back, but if not, its useless there
                                if len(guild_ids) > 0:
                                    others = True
                                    content_cl.append(
                                        f"{guild_ids}  {channel_ids}  {line_[2]}  {line_[3]}  {line_[4]}  {line_[5]}  {line_[6]}  {line_[7]}  {line_[8]}")
                            else:
                                content_cl.append(line_cl)
                        else:
                            content_cl.append(line_cl)
                        if guild_ids.__contains__(id_guild) and title == searched_title:
                            same_title = True
            if found is True:
                # I need to delete it from server_latest
                if others is False:
                    with open('server_latest', 'r', errors='ignore') as r_sl:
                        for line_sl in r_sl:
                            if line_sl != ' \n' or line_sl != '':
                                # Make sure theer will be no empty lines
                                line_ = line_sl.split("-+-")
                                title_ = f'{line_[1]}'
                                if line_[0] == str(source):
                                    if title_ != str(searched_title):
                                        content_sl.append(line_sl)
                                else:
                                    content_sl.append(line_sl)
                    # I need to delete it from server_release_ping
                    # Now I need to rewrite server_latest
                    with open('server_latest', 'w', errors='ignore') as w_sl:
                        for item in content_sl:
                            if not item.__contains__("\n"):
                                item += ' \n'
                            w_sl.write(item)
                if same_title is False:
                    with open('server_release_ping', 'r', errors='ignore') as r_srp:
                        for line_srp in r_srp:
                            if line_srp != ' \n' and line_srp != '':
                                line_split = line_srp.split('-+-')
                                if str(id_guild) == str(line_split[0]):
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
                            users = line_s[2].replace("[", "").replace("]", "").replace("'", '').replace("\\n",
                                                                                                         '').replace(
                                "\n", '').replace(" ", '').replace("  ", '').split(",")
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
                    dm_list = split_dm[1].replace("['", '').replace("']", '').replace("\n", '').replace("'",
                                                                                                        '').replace(' ',
                                                                                                                    '').split(
                        ',')
                    print(dm_list)
                    for s in dm_list:
                        s.replace(' ', '')
                        if s != '[]':
                            dm_ping.append(s)
                    print(dm_ping)
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


i = 0
@tasks.loop(minutes=30)
async def periodical_restart(i=i):
    await bot.wait_until_ready()
    is_first = getF(First)
    if i == 1:
        os.execl(sys.executable, sys.executable, *sys.argv)
        print('Restarted')
    else:
        i += 1
        print('30min left till reset')


@tasks.loop(seconds=60)
async def releaseCheck():
    release_check = await release.chapterreleasecheck(bot, announced)
#setAnnounced(release_check)


# <@401845652541145089>
setGuilds.start()
periodical_restart.start()
releaseCheck.start()
rich_presence.start()
bot.run('ODg3Mzc4NzM3MTQ5MTQ1MTI4.Gym1c8.N0QZ280R8KEauRaMKdynU5QuVi59GwtNXFYy0k')
