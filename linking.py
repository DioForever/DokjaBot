def link_read(guild_id: str):
    #855860264942829589-*-{1: ['LuminousScans-+-FFF-Class Trash Hero', 'MangaClash-+-FFF-Class Trashero']}
    #Guild id with dictionary of links

    # lets find the server linked
    with open("linked_server","r") as read:
        for line in read:
            guild_id_file, links = line.split("-*-")
            # lets check if its the same guild
            if guild_id_file == guild_id:
                # need to make a list from the str
                linked_unsorted = str(links).split("'")
                linked = {}
                link_curr = []
                link_num = 0
                for i in range(1,len(linked_unsorted)):
                    # if its a number, we have to add it to the directory
                    # and set the list to blank, so we can do new link
                    # check if its not 0, cuz we would get last item, which we dont wana
                    # or if its last, cuz we need to save even the last links
                    if (i != 0) or ((i+1) == len(linked_unsorted)):
                        # if its a new number
                        try_num = linked_unsorted[i - 1].strip('{').strip(': [').strip('], ')
                        if (try_num.isnumeric()) or ((i+1) == len(linked_unsorted)):
                            if link_curr != []:
                                linked.setdefault(link_num,link_curr)
                                link_curr = []
                            if (try_num.isnumeric()):
                                link_num = try_num
                    if (i+1) % 2 == 0:
                        link_curr.append(linked_unsorted[i])
    return linked

def link_check(guild_id: str, title: str, source: str, chapter: float):
    print(guild_id, title, source, chapter)
    # we call link_read to get the links of the server
    links = link_read(guild_id)
    print(links)
    # we gonna loop through and find if any of them has out curr source-+-title inside
    # if not the return False
    for key in links.keys():
        link_team = links[key]
    return False