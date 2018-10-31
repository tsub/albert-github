# -*- coding: utf-8 -*-

import json
import os
import re

from albertv0 import Item, UrlAction, FuncAction, ProcAction, cacheLocation
from urllib import request

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "GitHub"
__version__ = "0.1"
__trigger__ = "gh "
__author__ = "Tsubasa Takayama"
__dependencies__ = []

iconPath = "%s/%s.svg" % (os.path.dirname(__file__), __name__)
baseUrl = "https://api.github.com"
filePrefix = "{0}/{1}_".format(cacheLocation(), __prettyname__)
cachePath = filePrefix + "cache.json"
accessTokenPath = filePrefix + "access_token"


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


def deleteCache():
    if not os.path.isfile(cachePath):
        return

    os.remove(cachePath)


def saveAccessToken(accessToken):
    with open(accessTokenPath, mode="w") as f:
        f.write(accessToken)


def loadAccessToken():
    if not os.path.isfile(accessTokenPath):
        return

    with open(accessTokenPath) as f:
        return f.read()


def deleteAccessToken():
    if not os.path.isfile(accessTokenPath):
        return

    os.remove(accessTokenPath)


def fetchRepositories(endpoint, accessToken):
    responses = []

    headers = {
        "Authorization": "token {0}".format(accessToken)
    }
    req = request.Request(endpoint + "?page=0&per_page=100", headers=headers)
    with request.urlopen(req) as res:
        links = parseLinkHeader(res.getheader("Link"))
        responses.append(json.loads(res.read().decode()))

    while "next" in links:
        req = request.Request(links["next"], headers=headers)
        with request.urlopen(req) as res:
            links = parseLinkHeader(res.getheader("Link"))
            responses.append(json.loads(res.read().decode()))

    return responses


def fetchMyRepositories(accessToken):
    return fetchRepositories(baseUrl + "/user/repos", accessToken)


def fetchStarredRepositories(accessToken):
    return fetchRepositories(baseUrl + "/user/starred", accessToken)


def loadRepositories(accessToken):
    cachedData = loadCache()
    if cachedData:
        return json.loads(cachedData)

    multiResponses = []
    multiResponses.append(fetchMyRepositories(accessToken))
    multiResponses.append(fetchStarredRepositories(accessToken))

    repos = [
        repo for responses in multiResponses for repos in responses for repo in repos]
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

        accessToken = loadAccessToken()
        if not accessToken:
            if stripped:
                return Item(id=__prettyname__,
                            icon=iconPath,
                            text="Save your GitHub access token",
                            subtext="Require scope is \"repo\".",
                            actions=[
                                FuncAction("Save your GitHub access token",
                                           lambda: saveAccessToken(stripped))
                            ])
            else:
                return Item(id=__prettyname__,
                            icon=iconPath,
                            text="Please type your GitHub access token",
                            subtext="Require scope is \"repo\".")

        if stripped.startswith(">"):
            items = []
            items.append(Item(id=__prettyname__,
                              icon=iconPath,
                              text="Delete cached repositories",
                              subtext="Please refetch repositories after deleted. It takes a lot of time.",
                              actions=[
                                  FuncAction("Delete cached repositories",
                                             lambda: deleteCache())
                              ]))
            items.append(Item(id=__prettyname__,
                              icon=iconPath,
                              text="Delete your saved GitHub access token",
                              subtext="Please reconfigure your GitHub access token.",
                              actions=[
                                  FuncAction("Delete your saved GitHub access token",
                                             lambda: deleteAccessToken())
                              ]))

            return items

        results = []

        try:
            data = loadRepositories(accessToken)
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

    if query.string.startswith("g"):
        return Item(id=__prettyname__,
                    icon=iconPath,
                    text="gh",
                    subtext="Open GitHub repositories in browser",
                    completion="gh ",
                    actions=[
                        ProcAction("Complete gh trigger", [
                                   "albert", "show", "gh "])
                    ])
