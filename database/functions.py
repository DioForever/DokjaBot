import sqlite3
from enum import Enum


# MangaTable
# - title
# - link
# - r
# - g
# - b
#
# ServerTable
# - identifier = title+serverId PRIMARY KEY
# - titleMI
# - serverId
# - channelId
# - pings
# - link
#
# ShelfTable
# - shelfTitle
# - serverId
# - identifiers

class MangaItem:
    def __init__(self, title, link, r, g, b):
        self.title = title
        self.link = link
        self.r = r
        self.g = g
        self.b = b


class ServerItem:
    def __init__(self, identifier, titleMI, serverId, pings, link):
        self.identifier = identifier
        self.titleMI = titleMI
        self.serverId = serverId
        self.pings = pings
        self.link = link


class ShelfItem:
    def __init__(self, Title):
        self.name = Title


def switchSpecs(tableName: str):
    if tableName == "mangaTable":
        return "title, link, r, g, b", initiate_mt()
    elif tableName == "serverTable":
        return "titleMI, serverId, channelId, pings", initiate_st()
    elif tableName == "shelfTable":
        return "shelfTitle, serverId, identifiers", initiate_sht()
    else:
        return "", ""


def initiate_st():
    connection = sqlite3.connect('serverTable.db')
    cursor = connection.cursor()

    initCmd = ''' CREATE TABLE IF NOT EXISTS
    serverTable(identifier TEXT PRIMARY KEY,titleMI TEXT, serverId TEXT, channelId TEXT, pings TEXT, link TEXT) '''

    cursor.execute(initCmd)
    return connection


def initiate_mt():
    connection = sqlite3.connect('mangaTable.db')

    initCmd = ''' CREATE TABLE IF NOT EXISTS
    mangaTable(title TEXT, link TEXT, r INT, g INT, b INT) '''

    connection.execute(initCmd)
    return connection


def initiate_sht():
    connection = sqlite3.connect('shelfTable.db')

    initCmd = ''' CREATE TABLE IF NOT EXISTS
    shelfTable(shelfTitle TEXT, serverId TEXT, identifiers TEXT) '''

    connection.execute(initCmd)
    return connection


def select(tableName: str, selection: str, conditions: str):
    specs, connection = switchSpecs(tableName)
    if specs == "":
        return
    cursor = connection.execute(f"SELECT {selection} from {tableName}")
    for row in cursor:
        print(row)


def insert_new(tableName: str, values: list):
    specs, connection = switchSpecs(tableName)
    if specs == "":
        return False
    cmd = f"INSERT INTO {tableName} ({specs}) VALUES ("
    for num, value in enumerate(values):
        if isinstance(value, str):
            cmd += f"'{value}'"
        else:
            cmd += f"{value}"
        if num != len(values) - 1:
            cmd += ", "
        else:
            cmd += ")"
    print(cmd)
    connection.execute(cmd)
    connection.commit()
    connection.close()
    return True


def insert_update(tableName: str, values: list):
    specs, connection = switchSpecs(tableName)
    if specs == "":
        return False
    cmd = f"REPLACE INTO {tableName} ({specs}) VALUES ("
    for num, value in enumerate(values):
        if isinstance(value, str):
            cmd += f"'{value}'"
        else:
            cmd += f"{value}"
        if num != len(values) - 1:
            cmd += ", "
        else:
            cmd += ")"
    print(cmd)
    connection.execute(cmd)
    connection.commit()
    connection.close()
    return True


print(insert_new("mangaTable", ["FFF-Class Trashero", "https://trashero.com", 24, 126, 354]))
# print(select(select("mangaTable", "*")))
