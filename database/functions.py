import sqlite3


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

class MangaItem:
    def __init__(self, title, link, number, hexColor):
        self.title = title
        self.link = link
        self.number = number
        self.hexColor = hexColor


class ServerItem:
    def __init__(self, identifier, titleMI, serverId, pings, link, shelfName):
        self.identifier = identifier
        self.titleMI = titleMI
        self.serverId = serverId
        self.pings = pings
        self.link = link
        self.shelfName = shelfName


class ShelfItem:
    def __init__(self, Title):
        self.name = Title


def optimizeValues(values: list):
    valuesOpt = []
    for val in values:
        if isinstance(val, str):
            valuesOpt.append(val.replace("\n", ''))
        else:
            valuesOpt.append(val)
    return valuesOpt


def switchSpecs(tableName: str):
    if tableName == "mangaTable":
        return "title, link, number, hexColor", initiate_mt(f"database/mangaTable.db")
    elif tableName == "serverTable":
        return "identifier, titleMI, serverId, channelId, pings, link, shelfName", initiate_st(
            f"database/serverTable.db")
    elif tableName == "shelfTable":
        return "shelfTitle, serverId, identifiers", initiate_sht(f"database/shelfTable.db")
    else:
        return "", ""


def initiate_st(tableLocation: str):
    connection = sqlite3.connect(tableLocation)
    cursor = connection.cursor()

    initCmd = '''CREATE TABLE IF NOT EXISTS serverTable(identifier TEXT PRIMARY KEY,titleMI TEXT, serverId TEXT, 
    channelId TEXT, pings TEXT, link TEXT, shelfName TEXT)'''

    cursor.execute(initCmd)
    return connection


def initiate_mt(tableLocation: str):
    connection = sqlite3.connect(tableLocation)

    initCmd = ''' CREATE TABLE IF NOT EXISTS
    mangaTable(link TEXT PRIMARY KEY,title TEXT, number DECIMAL, hexColor TEXT) '''

    connection.execute(initCmd)
    return connection


def initiate_sht(tableLocation: str):
    connection = sqlite3.connect(tableLocation)

    initCmd = ''' CREATE TABLE IF NOT EXISTS
    shelfTable(shelfTitle TEXT PRIMARY KEY, serverId TEXT, identifiers TEXT) '''

    connection.execute(initCmd)
    return connection


def select(tableName: str, selection: str, conditions: str = ""):
    conditions = conditions.replace("\n", "")
    specs, connection = switchSpecs(tableName)
    if specs == "":
        return
    cmd = f"SELECT {selection} from {tableName}"
    if conditions != "": cmd += F" WHERE {conditions}"
    print(cmd)
    cursor = connection.execute(cmd)
    values = []
    for row in cursor:
        print(row)
        values.append(row)
    return values


def insert_new(tableName: str, values: list):
    values = optimizeValues(values)
    specs, connection = switchSpecs(tableName)
    if specs == "":
        return False
    cmd = f"INSERT OR IGNORE INTO {tableName} ({specs}) VALUES ("
    for num, value in enumerate(values):
        if isinstance(value, str):
            value = value.replace("\n", "")
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
    values = optimizeValues(values)
    specs, connection = switchSpecs(tableName)
    if specs == "":
        return False
    cmd = f"INSERT OR REPLACE INTO {tableName} ({specs}) VALUES ("
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


def addMangaTable(values):
    values = optimizeValues(values)
    insert_new("mangaTable", values)
    return True


def addServerTable(values):
    values = optimizeValues(values)
    identifier = "'" + values[0].replace("\n", "") + "'"
    print(f"ss {identifier} ss")
    selection = select("serverTable", f"identifier", f"identifier={identifier}")
    if len(selection) != 0:
        return False
    insert_new("serverTable", values)
    return True

# ServerTable
# - identifier = title+serverId PRIMARY KEY
# - titleMI
# - serverId
# - channelId
# - pings
# - link
# - shelfName
# print(insert_new("mangaTable", ["FFF-Class Trashero", "https://trashero.com", 145, #92908c]))
# (select("mangaTable", "*", "r=24"))
# insert_update("serverTable",
#               ["FFF-Class Trasher-1654797725", "FFF-Class Trashero", 1654797725, 125647812, "@154625412",
#                "https://trashero.com", "FFF-Class"])
