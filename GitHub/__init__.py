# -*- coding: utf-8 -*-

import json
import os

from albertv0 import Item, UrlAction, cacheLocation
from urllib import request

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "GitHub"
__version__ = "0.1"
__trigger__ = "gh "
__author__ = "Tsubasa Takayama"
__dependencies__ = []

iconPath = "%s/%s.svg" % (os.path.dirname(__file__), __name__)
baseUrl = "https://api.github.com"
cachePath = cacheLocation() + "/" + __prettyname__ + ".json"


def saveCache(repos):
    with open(cachePath, mode="w") as f:
        f.write(repos)


def loadCache():
    if not os.path.isfile(cachePath):
        return

    with open(cachePath) as f:
        return f.read()


def getRepositories():
    # TODO: Update cache
    cachedData = loadCache()
    if cachedData:
        return json.loads(cachedData)

    req = request.Request(baseUrl + "/users/tsub/repos?per_page=20")
    with request.urlopen(req) as res:
        data = res.read().decode()
        saveCache(data)

        return json.loads(data)


def filterByQuery(repos, query):
    return list(filter(lambda repo: repo["full_name"].find(query) > -1, repos))


def appendItem(items, repo):
    name = repo['full_name']
    description = repo['description'] or ""
    url = repo['html_url']

    item = Item(id=__prettyname__,
                icon=iconPath,
                text=name,
                subtext=description,
                actions=[
                   UrlAction("Open repository", url)
                ])

    return items + [item]


def noResultItem():
    return Item(id=__prettyname__,
                icon=iconPath,
                text="No results.")


def handleQuery(query):
    if query.isTriggered:
        stripped = query.string.strip()
        results = []
        data = getRepositories()

        repos = filterByQuery(data, stripped) if stripped else data

        for repo in repos:
            results = appendItem(results, repo)

        if results:
            return results

        return noResultItem()
