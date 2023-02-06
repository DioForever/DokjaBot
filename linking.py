def link_check(guild_id: str, title: str, chapter: float):
    #855860264942829589-*-[[LuminousScans-+-FFF-Class Trash Hero, MangaClash-+-FFF-Class Trashero]]
    #Guild id with List of lists linked mangas
    print(guild_id, title, chapter)
    # lets find the server linked
    with open("linked_server","r") as read:
        for line in read:
            guild_id_file, linked = line.split("-*-")
            # lets check if its the same guild
            if guild_id_file == guild_id:
                print(linked)
                # need to make a list from the str
                linked_unsorted = str(linked).split("]")
                linked = []
                for lined_item in linked_unsorted:

                print(linked_unsorted)


    return False