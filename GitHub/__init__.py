# -*- coding: utf-8 -*-

import json
import os
import re

from albertv0 import Item, UrlAction, cacheLocation
from urllib import request

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "GitHub"
__version__ = "0.1"
__trigger__ = "gh "
__author__ = "Tsubasa Takayama"
__dependencies__ = []

iconPath = "%s/%s.svg" % (os.path.dirname(__file__), __name__)
baseUrl = "https://api.github.com"
cachePath = cacheLocation() + "/" + __prettyname__ + ".json"


def parseLinkHeader(link_header):
    links = [l.strip() for l in link_header.split(',')]
    rels = {}
    pattern = r'<(?P<url>.*)>;\s*rel="(?P<rel>.*)"'
    for link in links:
        group_dict = re.match(pattern, link).groupdict()
        rels[group_dict['rel']] = group_dict['url']
    return rels


def saveCache(repos):
    with open(cachePath, mode="w") as f:
        f.write(repos)


def loadCache():
    if not os.path.isfile(cachePath):
        return

    with open(cachePath) as f:
        return f.read()


def fetchRepositories(endpoint):
    responses = []

    req = request.Request(endpoint + "?page=0&per_page=20")
    with request.urlopen(req) as res:
        links = parseLinkHeader(res.getheader("Link"))
        responses.append(json.loads(res.read().decode()))

    while "next" in links:
        req = request.Request(links["next"])
        with request.urlopen(req) as res:
            links = parseLinkHeader(res.getheader("Link"))
            responses.append(json.loads(res.read().decode()))

    return responses


def fetchMyRepositories():
    return fetchRepositories(baseUrl + "/users/tsub/repos")


def fetchStarredRepositories():
    return fetchRepositories(baseUrl + "/users/tsub/starred")


def loadRepositories():
    # TODO: Update cache
    cachedData = loadCache()
    if cachedData:
        return json.loads(cachedData)

    multiResponses = []
    multiResponses.append(fetchMyRepositories())
    multiResponses.append(fetchStarredRepositories())

    repos = [repo for responses in multiResponses for repos in responses for repo in repos]
    saveCache(json.dumps(repos))

    return repos


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

        try:
            data = loadRepositories()
        except Exception as err:
            return Item(id=__prettyname__,
                        icon=iconPath,
                        text="Error.",
                        subtext=str(err))

        repos = filterByQuery(data, stripped) if stripped else data

        for repo in repos:
            results = appendItem(results, repo)

        if results:
            return results

        return noResultItem()
