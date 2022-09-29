from datetime import datetime
import nextcord
import apis as api
import callables as call


# @tasks.loop(seconds=60)
async def chapterreleasecheck(bot, announced):
    # I need to wait till the bot is running
    await bot.wait_until_ready()
    channel_print = bot.get_channel(980509693329932338)
    start = datetime.now().strftime('%H:%M:%S')
    print(f'Refreshing releases status: Starting {start}')
    await channel_print.send(f'Refreshing releases status: Starting {start}')
    # I will read the channel listed file
    lines_cl = []
    with open("channel_listed", "r") as read_cl:
        for line_cl in read_cl:
            lines_cl.append(line_cl)
    # Now that I have the list of mangas I have to check, well, I have to check it
    for manga in lines_cl:
        manga_splited = manga.split("  ")
        guild_ids = manga_splited[0].replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
        channel_ids = manga_splited[1].replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
        title = manga_splited[3]
        source = manga_splited[4]
        urlbasic = manga_splited[5]
        r = manga_splited[6]
        g = manga_splited[7]
        b = manga_splited[8]
        release = api.getReleases(source, title, urlbasic, int(r), int(g), int(b), guild_ids)
        # return released, embed, subscription, chapter_number
        if release[0] is True:
            released = release[0]
            embed = release[1]
            subscription = release[2]
            chapter_number = release[3]
            urlbasic = release[4]
            urlchapter = release[5]
            chapter_num = release[6]
            message_release = release[7]
            sources_announced_already = release[8]
            url_thumb = release[9]
            chapters = release[10]
            # first I need to find out to which channels I already told it
            # cuz I got manga with same title maybe advanced
            with open("channel_listed", "r") as read_cl:
                for line_cl in read_cl:
                    split_line_cl = line_cl.split("  ")
                    guild_ids_cl = manga_splited[0].replace("[", "").replace("]", "").replace(" ", "").replace("'","").split(",")
                    channel_ids_cl = manga_splited[1].replace("[", "").replace("]", "").replace(" ", "").replace("'","").split(",")
                    title_cl = manga_splited[3]
                    source_cl = manga_splited[4]
                    if title_cl == title and sources_announced_already.__contains__(str(source_cl)):
                        for ch_id in channel_ids_cl:
                            if channel_ids.__contains__(ch_id):
                                channel_ids.remove(ch_id)

            count = 0
            for channel_id in channel_ids:
                channel = bot.get_channel(int(channel_id))
                dominant_color = call.get_dominant_color(url_thumb)
                file = nextcord.File("img.png", filename="img.png")
                embed.set_image(url="attachment://img.png")
                await channel.send(file=file, embed=embed)
                guild_id = guild_ids[count]
                ping_types = call.sortAnnounce(guild_id, subscription)
                dm = ping_types[0]
                ping = str(ping_types[1]).replace("[","").replace("]","").replace("'","")
                if len(ping) > 0:
                    embed_pings = nextcord.Embed(title=f"Ping",
                                               description=f"Yo, just pinging ya, cuz u wana know about this \n",
                                               color=nextcord.Color.from_rgb(255, 200, 0))
                    await channel.send(embed=embed_pings)
                    await channel.send(ping)
                server = bot.get_guild(int(guild_id))
                embed_user = nextcord.Embed(title=f"{title}", url=f"{urlbasic}",
                                           description=f"The Chapter/s {chapters} was released! \n"
                                                       f" Link to the chapter: {urlchapter} \n"
                                                       f" Server: {server}",
                                           color=nextcord.Color.from_rgb(int(r), int(g), int(b)))
                file = nextcord.File("img.png", filename="img.png")
                embed_user.set_image(url="attachment://img.png")
                for user_id in dm:
                    user_id = user_id.replace("<@","").replace(">","")
                    user = await bot.fetch_user(user_id)
                    await user.send(file=file, embed=embed_user)

                count += 1

    end = datetime.now().strftime('%H:%M:%S')
    print(f'Refreshing releases status: Finished {end}')
    await channel_print.send(f'Refreshing releases status: Finished {end}')

