# coding: utf-8

import requests, clipboard, webbrowser

html = requests.get("http://www.twitter.com/jessemillar").text

index = html.find("Followers</span>")
followers = html[index+82:index+85]

clipboard.set("@jessemillar has " + followers + " Twitter followers.")

webbrowser.open("workflow://")