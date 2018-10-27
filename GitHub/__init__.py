# -*- coding: utf-8 -*-

import json
import os

from albertv0 import Item, UrlAction
from urllib import request

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "GitHub"
__version__ = "0.1"
__trigger__ = "gh "
__author__ = "Tsubasa Takayama"
__dependencies__ = []

iconPath = "%s/%s.svg" % (os.path.dirname(__file__), __name__)
baseUrl = "https://api.github.com"


def getRepositories():
    # TODO: To cache reposonse
    req = request.Request(baseUrl + "/users/tsub/repos?per_page=20")
    with request.urlopen(req) as res:
        return json.loads(res.read().decode())


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
