#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: dork.py
# Created: Wednesday, 16th December 2020 9:23:18 pm
# Author: Rakibul Yeasin (ryeasin03@gmail.com)
# -----
# Last Modified: Tuesday, 22nd December 2020 3:09:39 am
# Modified By: Rakibul Yeasin (ryeasin03@gmail.com)
# -----
# Copyright (c) 2020 Slishee
###

import os
import re
import sys
import requests as rq
from urllib.parse import unquote
from random import randint

# Multithread
from threading import Thread

from requests.models import HTTPError

"""
To-Do:
    - Add google search method implemented in gopher
    - Add more search-engines
    - Handle some more common errors
    - Input from file (dorklist)
"""

def get_dorks() -> list:
    with open('dork.txt', 'r') as f:
        dorks = f.readlines()
    return dorks

def filter(url: str) -> str:
    """
    Only allows urls with '?'
    """
    if url.find("?") != -1: return url

def filter_ms(url):
    regex = r".*(http.*\/.*)"
    new_url = re.findall(regex, url)
    return new_url[0]

def ask(dork: str, *args: tuple) -> None:
    """
    Searches in `https://ask.com`
    """
    # We assume max-page number is 200
    for i in range(1, 201):
        url = f"https://www.ask.com/web?q={dork}&qsrc=998&page={i}"
        # data = BeautifulSoup(rq.get(url).text, "html.parser")
        # findings = data.find_all("a", {"class": "PartialSearchResults-item-title-link result-link"})
        # for f in findings:
        #     if filter(f["href"]) is not None: storage.write(f["href"] + "\n")
        data = rq.get(url).text
        with open('data.txt', 'w') as f:
            f.write(data)
        regex = r'\<p\sclass\=\"PartialSearchResults-item-url\"\>(.*?)\<\/p\>'
        urls = re.findall(regex, data)
        for i in urls:
            if filter(i):
                print(f"[+] Found: http://{unquote(i)}")
                storage.write(f"http://{unquote(i)}\n")

def bing(dork: str, *args: tuple) -> None:
    """
    Searches in `https://ask.com`
    """

    # bing.com returns plain html for mobile. For Desktop it responds with js
    headers = {
        "User-Agent": "Opera/9.80 (Android; Opera Mini/12.0.1987/37.7327; U; pl) Presto/2.12.423 Version/12.16"
    }

    # We assume max-page number is 200
    for i in range(1, 201):
        url = f"https://www.bing.com/search?q={dork}&first={i}&FORM=PERE"
        data = rq.get(url, headers=headers).text
        http = re.findall(r'<a\shref=\"http:\/\/(.*?)\">', data)
        https = re.findall(r'<a\shref=\"https:\/\/(.*?)\">', data)
        http = ["http://"+i for i in http]
        https = ["https://"+i for i in https]
        links = [*http, *https]
        for l in links:
            a = unquote(l).split(" ")[0].replace('"', '')
            if l.find("www.microsofttranslator.com") != -1:
                a = filter_ms(a)
            if filter(a):
                print(f"[+] Found: {unquote(a)}")
                storage.write(f"{unquote(a)}\n")

def google(dork: str, *args: tuple) -> None:
    """
    Searches in `https://cse.google.com`
    `cse.google.com` is google custom search engine that is intended to use
    is websites to bring on google powerful search in that.

    Google provides a JavaScript code that calls ajax(XMLHttpRequest) request
    with a csrf-token and referer as self.

    Note: We intend to use 'gophers' method in future
    """

    # We need to refer from `https://cse.google.com`
    headers = {
        "Referer": "https://cse.google.com/cse?cx=partner-pub-2698861478625135:3033704849",
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.{randint(000, 333)}.169 Safari/537.36"
    }

    i = 1
    # Goole has a lot more pages to provide search results
    # Why should we bother counting them!
    while True:
        url = "https://cse.google.com/cse.js?hpg=1&cx=partner-pub-2698861478625135:3033704849"
        data = rq.get(url, headers=headers).text
        regex = r"\"cse_token\":\s\".*\""
        # Here we get the csrf-token
        cse_token = re.findall(regex, data)
        if cse_token is not None:
            tk = cse_token[0].replace('"cse_token": "', "").replace('"', "")
            nurl = f"https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&&start={i}&hl=en&source=gcsc&gss=.com&cselibv=921554e23151c152&cx=partner-pub-2698861478625135:3033704849&q={dork}&safe=off&cse_tok={tk}&exp=csqr,cc&callback=google.search.cse.api16950"
            res = rq.get(nurl, headers=headers).text
            regex = r'\"url\":\s\"(.*)\"'
            urls = re.findall(regex, res)
            if urls:
                urls.pop()
                if urls is not None:
                    for res_url in urls:
                        if res_url.startswith("http") and filter(res_url):
                            print(f"[+] Found: {unquote(res_url)}")
                            storage.write(unquote(res_url) + "\n")
        # Increment Page Number
        i += 1

if __name__ == "__main__":
    PATH = os.path.join(os.getcwd(), "url-list.txt")
    storage = open(PATH, "a")
    try:
        for dork in get_dorks():
            # Threads
            threads = []
            ask_com = Thread(target=ask, args=dork)
            bing_com = Thread(target=bing, args=dork)
            google_com = Thread(target=google, args=dork)

            # Start Threads
            ask_com.start()
            bing_com.start()
            google_com.start()
            threads.append(ask_com)
            threads.append(bing_com)
            threads.append(google_com)
            for t in threads:
                t.join()

            # Plain
            # ask(dork)
            # bing(dork)

    except KeyboardInterrupt:
        storage.close()
        sys.exit()

    except ValueError:
        sys.exit()

    except Exception as e:
        print(e)
    # We should hanle more errors like: HTTPError and so on
    finally:
        storage.close()
        sys.exit()
    storage.close()
