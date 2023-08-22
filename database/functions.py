import sqlite3


# MangaTable
# - title
# - link
# - r
# - g
# - b
#
# ServerTable
# - identifier = title+serverId
# - titleMi
# - serverId
# - channelId
# - pings

def switchSpecs(tableName: str):
    if tableName == "mangaTable":
        return "title, link, r, g, b", initiate_mt()
    elif tableName == "serverTable":
        return "titleMI, serverId, channelId, pings", initiate_st()
    else:
        return "", ""


def initiate_st():
    connection = sqlite3.connect('serverTable.db')
    cursor = connection.cursor()

    initCmd = ''' CREATE TABLE IF NOT EXISTS
    serverTable(identifier TEXT PRIMARY KEY,titleMI TEXT, serverId TEXT, channelId TEXT, pings TEXT) '''

    cursor.execute(initCmd)
    return connection


def initiate_mt():
    connection = sqlite3.connect('mangaTable.db')

    initCmd = ''' CREATE TABLE IF NOT EXISTS
    mangaTable(title TEXT, link TEXT, r INT, g INT, b INT) '''

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
        if num != len(values)-1:
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
        if num != len(values)-1:
            cmd += ", "
        else:
            cmd += ")"
            cmd += ")"
    print(cmd)
    connection.execute(cmd)
    connection.commit()
    connection.close()
    return True


print(insert_new("mangaTable", ["FFF-Class Trashero", "https://trashero.com", 24, 126, 354]))
# print(select(select("mangaTable", "*")))
