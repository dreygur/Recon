#!/usr/bin/env python3

"""
Filename: Recently Patched Scrapper.py
Author: Rakibul Yeasin (@dreygur)
Last Modified; 10/01/2021
"""

import re
import requests as rq
from bs4 import BeautifulSoup

# Multiprocess
import multiprocessing as mp

def scrape(uri):
    data = rq.get(uri).text
    reg = r'.*cell1\"\>\<a\shref=.[/a-z0-9\">]{19}(.[a-z0-9\.-]{,100}).[</a-z>]'
    links = re.findall(reg, data)
    return links

def save(data, *args):
    with open("out.txt", "a", encoding='utf-8') as f:
        print(f"[+] {data}")
        f.write(data + "\n")

def main():
    pool = mp.Pool(mp.cpu_count())
    uri = "https://www.openbugbounty.org/patched/page/"
    for i in range(1, 100):
        data = scrape(f"{uri}{i}/")
        pool.map(save, data)
    pool.close()

if __name__ == "__main__":
    main()
