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


def addManga(url: str, interaction: Interaction):
    episodes, title, thumb = gateway(url)
    hexColor = get_dominant_color(thumb)
    number: float = 0
    if len(list(episodes.keys)) > 0:
        number = episodes[list(episodes.keys)[0]]
    print([url, title, number, hexColor])

    addMangaTable([url, title, number, hexColor])

    serverId = 00000000
    channelId = 0000000
    identifier = f"{title}{serverId}"
    pings = ""
    link = url
    shelfName = ""

    addServerTable([identifier, title, serverId, channelId, pings, link, shelfName])
    return True


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
