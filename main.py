from nextcord.ext import tasks, application_checks
from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from commands import basic

# from nextcord.ext import Interaction
import os
import sys

from manga.universal import createEmbed

allowed_mentions = nextcord.AllowedMentions(roles=True)
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


# serverID = 855860264942829589


# await bot.wait_until_ready()
print("DokjaBot activated - Made by DioForever - dioforever.live")


async def no_perms(interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        embed = nextcord.Embed(title=f"Required Channel management perms!",
                               color=nextcord.Color.from_rgb(255, 0, 0))
        await interaction.response.send_message(embed=embed, delete_after=5)
    else:
        raise error


@tasks.loop(seconds=60)
async def rich_presence():
    await bot.wait_until_ready()
    guilds = bot.guilds
    number_of_servers = len(guilds)
    await bot.change_presence(status=nextcord.Status.online,
                              activity=nextcord.Game(f'Library of Culture on {number_of_servers} servers'), )


@bot.slash_command(guild_ids=serverID)
async def add_manga(interaction: nextcord.Interaction, url: str, ping: str, shelf_name: str):
    """Repeats your message that you send as an argument

    Parameters
    ----------
#     interaction: Interaction
#         The interaction object
#     url: str
#         Link to the specific manga.
#     pings: str
#         Ping of the roles you want to be pinged upon new release
#     shelf_name: str
#         Name of a 'Shelf' or a Group of mangas of the same name but different source so it doesnt ping same chapter twice.
    """
    # await interaction.response.send_message(f"You said: {url, ping, shelf_name}")
    response: bool
    response, e, embed = basic.addManga(url, interaction, ping, shelf_name)
    if response is True and e is None:
        interaction.response.send(embed=embed, delete_after=15)
    else:
        print("FAIL", e)


# @bot.slash_command(guild_ids=serverID)
# async def ping(interaction: nextcord.Interaction, url: str, pings: str, shelfName: str):
#     """Add some new Manhua, Manhwa or Manga to your servers library!
#
#     Parameters
#     ----------
#     interaction: Interaction
#         The interaction object
#     url: str
#         Link to the specific manga.
#     pings: str
#         Ping of the roles you want to be pinged upon new release
#     shelfName: str
#         Name of a 'Shelf' or a Group of mangas of the same name but different source so it doesnt ping same chapter twice.
#     """
#     await interaction.response.send_message("Pong!")


# @bot.slash_command(name="add", description="Add some new Manhua, Manhwa or Manga to your servers library.",
#                    guild_ids=serverID, dm_permission=False)
# @application_checks.has_permissions(manage_channels=True)
# async def addManga(interaction: Interaction, url: str, pings: str, shelfName: str):
#     response: bool
#     response, e, embed = basic.addManga(url, interaction, pings, shelfName)
#     if response is True and e is None:
#         interaction.response.send(embed=embed, delete_after=15)
#
#
# @addManga.error
# async def permsError(interaction: Interaction, error):
#     await no_perms(interaction, error)


# @tasks.loop(seconds=60)
# async def releaseCheck():
#     await release.chapterreleasecheck(bot, announced)


# <@401845652541145089>
setGuilds.start()
# releaseCheck.start()
# rich_presence.start()
bot.run(open("botToken", "r").read())
