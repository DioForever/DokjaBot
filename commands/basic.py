import sys
import time

import nextcord
from nextcord import Interaction, PartialInteractionMessage, WebhookMessage
import asyncio
import threading

from manga.universal import gateway
from manga.universal import get_dominant_color
from manga.universal import createEmbed
from database.functions import addMangaTable
from database.functions import addServerTable


# MangaTable
# - link PRIMARY KEY
# - title
# - number
# - hexColor
#
# ServerTable
# - identifier = title+serverId PRIMARY KEY
# - titleMI
# - serverId
# - channelId
# - pings
# - link
# - shelfName
#
# ShelfTable
# - shelfTitle = serverId+serverId PRIMARY KEY
# - serverId
# - identifiers

class taskResponse:
    def __init__(self, interaction: Interaction, message: PartialInteractionMessage | WebhookMessage, edit: bool,
                 embed: nextcord.Embed):
        self.interaction = interaction
        self.message = message
        self.edit = edit
        self.embed = embed


class taskManga:
    def __init__(self, interaction: nextcord.Interaction, message: PartialInteractionMessage | WebhookMessage, url: str,
                 ping: str, shelf_name: str):
        self.interaction = interaction
        self.message = message
        self.url = url
        self.ping = ping
        self.shelf_name = shelf_name


taskMemory: list[taskManga] = []
taskResponseMemory: list[taskResponse] = []


# MANGA SECTION STARTS HERE---------------------------------------------------------------------------------------------

# This is the order
# I call manga_add_cmd, and it calls manga_add_call() which creates space for async function manga_add
# manga_add()
# manga_add_call()
# manga_add_work()
# addManga()
# Its like this because I have async function cmd and my functions take too long, so I schedule
# them and using threading I finish them at the same time

def addManga(url: str, interaction: Interaction, pings, shelfName=""):
    episodes: dict
    title: str
    thumb: str
    episodes, title, thumb = gateway(url)
    title = title.replace("\n", '')
    if episodes is None:
        return False, "Unsupported source", ""
    hexColor = get_dominant_color(thumb)
    number: float = 0
    print("-*-*-*-")
    print(episodes.keys)
    print(episodes)
    print("-*-*-*-")
    if len(episodes) > 0:
        number = next(iter(episodes))
    print([url, title, number, hexColor])
    if hexColor is None:
        hexColor: str = "#FFD700"
    addMangaTable([url, title, number, hexColor])

    serverId = interaction.guild_id
    channelId = interaction.channel_id
    identifier = f"{title}{serverId}"
    link = url

    addedBool: bool = addServerTable([identifier, title, serverId, channelId, pings, link, shelfName])
    e: Exception = Exception(sys.exception())
    print(f"already? {addedBool}")
    if addedBool is False:
        embedAlready = createEmbed(f"Attempt duplicate",
                                   f"Manga '{title}' has been found already in the library", "", "#e4b400")
        return True, e, embedAlready
    embedNew = createEmbed(f"Attempt successful", f"Manga '{title}' has been successfully added to the library \n"
                                                  f"shelfName: '{shelfName}'", "", "#00FF22")

    return True, e, embedNew


class workManga:
    def __init__(self, interaction: nextcord.Interaction, message, url: str, ping: str, shelf_name: str):
        threading.Thread(target=manga_work, args=(interaction, message, url, ping, shelf_name)).start()


#
# def manga_add_call(interaction: nextcord.Interaction, message, url: str, ping: str, shelf_name: str):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(manga_add_work(interaction, message, url, ping, shelf_name))
#     loop.close()


# async def manga_add_work(interaction: nextcord.Interaction, message, url: str, ping: str, shelf_name: str):
def manga_work(interaction: nextcord.Interaction, message: PartialInteractionMessage | WebhookMessage, url: str,
               ping: str, shelf_name: str):
    """Repeats your message that you send as an argument

    Parameters
    ----------
     interaction: Interaction
         The interaction object
     message:

     url: str
         URL of specific manga.
     ping: str
         Ping of the roles you want to be pinged upon new release
     shelf_name: str
         Name of a 'Shelf' or a Group of Mangas with the same name but different source so it doesn't ping same chapter twice.
    """
    print("finish line?")
    response: bool
    e: Exception
    response, e, embed = addManga(url, interaction, ping, shelf_name)
    print(response, type(e), e)
    if response is True:
        taskResp = taskResponse(interaction, message, True, embed)
        taskResponseMemory.append(taskResp)
        # message.edit(embed=embed)
        #  asyncio.wait_for(interaction.send(embed=embed), None)
        # await interaction.send(embed=embed)
        # await interaction.send(embed=embed, delete_after=15)

    else:
        embedFailed = createEmbed(f"Manga attempt falied",
                                  f"Manga with URL'{url}' has failed \n"
                                  f"Error: {e}", "", "#FF0000")
        taskResp = taskResponse(interaction, message, True, embedFailed)
        taskResponseMemory.append(taskResp)
        # message.edit(embed=embedFailed)
        # await interaction.send(embed=embedFailed)

        # await interaction.send(embed=embedFailed, delete_after=15)
        print("FAIL", e)


# MANGA SECTION ENDS HERE-----------------------------------------------------------------------------------------------
def removeManga():
    pass


def addPing():
    pass


def removePing():
    pass


def createLink():
    pass


def connectLink():
    pass


def disconnectLink():
    pass


def helpInfo():
    pass
