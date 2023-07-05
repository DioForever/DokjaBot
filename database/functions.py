import sqlite3


def initiate_st():
    connection = sqlite3.connect('serverTable.db')
    cursor = connection.cursor()

    initCmd = """CREATE TABLE IF NOT EXISTS
    serverTable(serverId TEXT PRIMARY KEY, mangaRef TEXT)"""

    cursor.execute(initCmd)
    return cursor


def initiate_mt():
    connection = sqlite3.connect('mangaTable.db')
    cursor = connection.cursor()

    initCmd = """CREATE TABLE IF NOT EXISTS
    mangaTable(title TEXT, link TEXT, r INT, g INT, b INT, ping TEXT)"""

    cursor.execute(initCmd)
    return cursor


def select(tableName: str, selection: str):
    cursor = initiate_st()
    cursor.execute(f"SELECT {selection} FROM {tableName}")
    result = cursor.fetchall()
    return result


def insert_new(tableName: str, values: str):
    cursor = initiate_st()
    cursor.execute(f"INSERT INTO {tableName} VALUES {values.capitalize()}")
