# -*- coding: utf-8 -*-

import json

from albertv0 import Item, iconLookup, UrlAction
from urllib import request

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "GitHub"
__version__ = "0.1"
__trigger__ = "gh "
__author__ = "Tsubasa Takayama"
__dependencies__ = []

iconPath = iconLookup("user-trash-full")
baseUrl = "https://api.github.com"


def handleQuery(query):
    if query.isTriggered:
        stripped = query.string.strip()

        if stripped:
            # WIP
            return Item(id=__prettyname__,
                        icon=iconPath,
                        text=query.string)
        else:
            results = []

            req = request.Request(baseUrl + "/users/tsub/repos?per_page=20")
            with request.urlopen(req) as res:
                data = json.loads(res.read().decode())

                for repo in data:
                    name = repo['full_name']
                    description = repo['description'] or ""
                    url = repo['html_url']

                    results.append(Item(id=__prettyname__,
                                        icon=iconPath,
                                        text=name,
                                        subtext=description,
                                        actions=[
                                           UrlAction("Open repository", url)
                                        ]))

                if results:
                    return results

                return Item(id=__prettyname__,
                            icon=iconPath,
                            text="No results.")
