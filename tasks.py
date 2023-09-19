import threading
import time

import aiohttp
import nextcord
import requests
from nextcord import Interaction, PartialInteractionMessage, WebhookMessage
import asyncio
import threading
import queue
import cloudscraper


class taskResponse:
    def __init__(self, interaction: Interaction, message: PartialInteractionMessage | WebhookMessage, edit: bool,
                 embed: nextcord.Embed):
        self.interaction = interaction
        self.message = message
        self.edit = edit
        self.embed = embed


class taskManga:
    def __init__(self, interaction: nextcord.Interaction, message: PartialInteractionMessage | WebhookMessage, url: str,
                 ping: str, shelf_name: str):
        self.interaction = interaction
        self.message = message
        self.url = url
        self.ping = ping
        self.shelf_name = shelf_name


class taskRequest:
    def __init__(self, url: str, function):
        self.url = url
        self.function = function


taskReq = taskRequest("https://aquamanga.com/read/fff-class-trash-hero/", "")
# taskMemory: list[taskManga] = []
taskReqMemory: list[taskRequest] = [taskReq]
taskResMemory: list[taskResponse] = []

with open("valid_proxies", "r") as f:
    proxies = f.read().split("\n")
print(proxies)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

# worked = False
# for proxy in proxies:
#     if worked is False:
#         print(f"trying {proxy}")
#         try:
#             req = requests.get("https://ww6.mangakakalot.tv/manga/manga-gi983617",
#                                proxies={'http': proxy, 'https': proxy, }, headers=headers)
#             # 35.206.200.71:3128 works
#             worked = True
#             print(req.text)
#             print(req.content)
#             print(proxy)
#         except Exception as e:
#             print(f"failed {e}")
#             continue
#


# @tasks.loop(seconds=60)
# async def taskManager():
#     proxy = "144.49.99.214"
#     for task in taskReqMemory.copy():
#         if isinstance(task, taskRequest):
#             res = requests.get("",
#                                proxies=(proxy, proxy))

# asyncio.run(taskManager())
