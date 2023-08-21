import sqlite3


def initiate_st():
    connection = sqlite3.connect('serverTable.db')
    cursor = connection.cursor()

    initCmd = """CREATE TABLE IF NOT EXISTS
    serverTable(titleMI TEXT,serverId TEXT)"""

    cursor.execute(initCmd)
    return cursor


def initiate_mt():
    connection = sqlite3.connect('mangaTable.db')
    cursor = connection.cursor()

    initCmd = """CREATE TABLE IF NOT EXISTS
    mangaTable(title TEXT, link TEXT, r INT, g TEXT, b TEXT)"""

    cursor.execute(initCmd)
    return cursor


def select(tableName: str, selection: str):
    if tableName == "mangaTable":
        cursor = initiate_mt()
    else:
        cursor = initiate_st()
    cursor.execute(f"SELECT {selection} FROM {tableName}")
    result = cursor.fetchall()
    return result


def insert_new(tableName: str, val: list):
    if tableName == "mangaTable":
        cursor = initiate_mt()
    else:
        cursor = initiate_st()
    print(f"INSERT INTO {tableName} ({val[0]}, {val[1]}, {val[2]}, {val[3]}, {val[4]})")

    print(cursor.execute('''SELECT * FROM mangaTable '''))



insert_new("mangaTable", ["FFF", "li0nk", "20", "1", "6"])
print("added")
print(select("mangaTable", "*"))
