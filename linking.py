def link_read(guild_id: str):
    #855860264942829589-*-{1: ['LuminousScans-+-FFF-Class Trash Hero', 'MangaClash-+-FFF-Class Trashero']}
    #Guild id with dictionary of links
    linked = {}
    # lets find the server linked
    with open("linked_server","r") as read:
        for line in read:
            guild_id_file, links = line.split("-*-")
            # lets check if its the same guild
            if guild_id_file == guild_id:
                # need to make a list from the str
                linked_unsorted = str(links).split("'")
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
    return dict(linked)

def link_write(type: int,guild_id: str, links: dict):
    # type 0 = edit
    # type 1 = add
    if type == 0:
        existing = []
        with open("linked_server","r") as read:
            for line in read:
                if not line.__contains__(guild_id):
                    existing.append(line)
        with open("linked_server","w") as write:
            write.write(str(links))
            for l in line:
                write.write(l)
    elif type == 1:
        existing = []
        with open("linked_server","r") as read:
            for line in read:
                existing.append(line)
        with open("linked_server","w") as write:
            write.write(str(links))
            for l in line:
                write.write(l)
    pass
def link_check(guild_id: str, title: str, source: str, chapter: float):
    # we call link_read to get the links of the server
    links = link_read(guild_id)
    # we gonna loop through and find if any of them has out curr source-+-title inside
    # if not the return False
    full_name = f"{source}-+-{title}"
    for key in links.keys():
        link_team = list(links[key])
        if link_team.__contains__(full_name):
            search_list = link_team
            search_list.remove(full_name)
            for search_item in search_list:
                source_search, title_search = str(search_item).split("-+-")
                if search_manga(source_search, title_search) >= chapter:
                    return True
    return False

def search_manga(source: str, title: str):
    with open("server_latest","r") as read:
        for line in read:
            source_read, title_read, chapter_read = line.split("-+-")
            if source_read == source and title_read == title:
                return float(chapter_read)

    return 0

def create_link(guild_id: int, source:str, title: str, source_1: str, title_1: str):
    existing = []
    # if its empty, server hasnt used linking yet
    links = link_read(str(guild_id))
    if links != []:
        # next we check if either one of those items hasnt already beed added to any link
        duplicated = False
        for key in links.keys():
            link_team = links[key]
            if link_team.__contains__(f"{source}-+-{title}"):
                duplicated = True
                break
            if link_team.__contains__(f"{source_1}-+-{title_1}"):
                duplicated = True
                break
        if not duplicated:
            # if not empty, we get the len+1 and set it as a new key
            links.setdefault(len(links) + 1, [f'{source}-+-{title}', f'{source_1}-+-{title_1}'])
            link_write(0, str(guild_id), links)
        else:
            # return saying its a duplicate
            pass

    else:
        links.setdefault(len(links)+1, [f'{source}-+-{title}', f'{source_1}-+-{title_1}'])
        link_write(1, str(guild_id), links)

def remove_link(guild_id: int, link_number: int):
    try:
        links = dict(link_read(str(guild_id)))
        links.pop(link_number-1)
        used_keys = links.keys()
        # we need to move all the keys higher than the one we deleted one level down
        # for example we delete 2 out of 1 2 3 4, we let 1 be and move 3,4 one level down and 3,4 becomes 2,3
        for link_num in range(link_number+1, len(links)):
            links[link_num-1] = links.pop(link_num)
    except:
        return False
    return True

def list_links(guild_id: int):
    pass