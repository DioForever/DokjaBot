import threading
import queue

from selenium import webdriver
import time

import bs4
import requests
from bs4 import BeautifulSoup

q = queue.Queue()
valid_proxies = []
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}


def getFreeProxyList():
    req = requests.get("https://free-proxy-list.net")
    html = BeautifulSoup(req.content, 'html.parser')

    proxies = (html.text.split('\n\n')[1]).split('\n')
    proxies.pop(-1)
    for prox in proxies:
        q.put(prox)


def check_proxies():
    global q
    while not q.empty():
        prox = q.get()
        proxy = {
            'http': prox,
            'https': prox,
        }
        try:
            res = requests.get("http://ipinfo.io/json",
                               proxy, timeout=10,
                               headers=headers)

        except Exception as e:
            # print(f"Fail proxy {proxy} - {e}")
            continue
        # print(res.text)
        # if not res.text.__contains__("Just a moment"):
        if res.status_code == 200:
            valid_proxies.append(prox)
            if len(valid_proxies) >= 15:
                break
            # print(f"trying {prox} PASSED")
        # else:
        # print(f"trying {prox} FAILED")


def updateValidProxies():
    getFreeProxyList()
    for _ in range(20):
        threading.Thread(target=check_proxies()).start()
    # print(valid_proxies)
    writeValidProxies()


def writeValidProxies():
    with open("proxies.txt", "w") as f:
        for proxy in valid_proxies:
            f.write(f"{proxy}\n")


updateValidProxies()
