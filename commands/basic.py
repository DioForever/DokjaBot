import sys

from nextcord import Interaction
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
        number = episodes[next(iter(episodes))]
    print([url, title, number, hexColor])

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
