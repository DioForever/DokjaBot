from datetime import datetime
import discord
import apis as api


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
        guild_ids = manga_splited[0].replace("[","").replace("]","").replace("'","").split(",")
        channel_ids = manga_splited[1].replace("[","").replace("]","").replace("'","").split(",")
        title = manga_splited[3]
        source = manga_splited[4]
        urlbasic = manga_splited[5]
        r = manga_splited[6]
        g = manga_splited[7]
        b = manga_splited[8]
        rHour = manga_splited[9]
        rMin = manga_splited[10]
        rDay = manga_splited[11]

        release = api.getReleases(source, title, urlbasic, int(r), int(g), int(b), guild_ids)
        # return released, embed, subscription, chapter_number
        if release[0] is True:
            released = release[0]
            embed = release[1]
            subscription = release[2]
            chapter_number = release[3]

            for channel_id in channel_ids:
                channel = bot.get_channel(int(channel_id))
                await channel.send(embed=embed)

    end = datetime.now().strftime('%H:%M:%S')
    print(f'Refreshing releases status: Finished {end}')
    await channel_print.send(f'Refreshing releases status: Finished {end}')

