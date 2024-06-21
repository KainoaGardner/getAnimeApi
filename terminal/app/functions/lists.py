from app import APIBASE, TerminalColor
import requests
import webbrowser
import json


def lists(args):
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "user" not in json_object:
            print(TerminalColor.BOLD + "---Not logged in---" + TerminalColor.END)
        else:
            user_id = json_object["user"]["id"]

            if "today" in args.list or "t" in args.list:
                list_today(user_id)
            elif "watchlist" in args.list or "wl" in args.list:
                list_watchlist(user_id)
            elif "all" in args.list or "a" in args.list:
                list_all(user_id)


def list_today(user_id):
    user_response = requests.get(APIBASE + f"users/list/{user_id}/today").json()

    print(TerminalColor.BOLD + "---Airing Today---" + TerminalColor.END)
    for count, anime in enumerate(user_response["result"]):
        print(
            TerminalColor.BOLD + f"{count + 1} ID: " + anime[1] + TerminalColor.END,
            end=" ",
        )
        print(anime[0])


def list_watchlist(user_id):
    user_response = requests.get(APIBASE + f"users/list/{user_id}/watchlist")
    print(
        TerminalColor.BOLD + "---Watchlist---" + TerminalColor.END,
    )
    for count, anime in enumerate(user_response.json()["data"]):
        print(
            TerminalColor.BOLD + f"{count + 1} " + anime[1] + TerminalColor.END,
            end=" ",
        )
        print(anime[0])


def list_all(user_id):
    print(TerminalColor.BOLD + "---Getting Shows---" + TerminalColor.END)
    user_response = requests.get(APIBASE + f"users/list/{user_id}/all")
    for count, anime in enumerate(user_response.json()["anime"]):
        print(
            TerminalColor.BOLD + f"{count + 1} " + anime[1] + TerminalColor.END,
            end=" ",
        )
        print(anime[0])


def nyaa():
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "user" not in json_object:
            print(TerminalColor.BOLD + "---Not logged in---" + TerminalColor.END)
        else:
            user_id = json_object["user"]["id"]
            print(TerminalColor.BOLD + "---Opened Nyaa Links---" + TerminalColor.END)

            airing_today = list_nyaa(user_id)
            for anime in airing_today:
                title = anime[0].lower()
                title = title.replace(" ", "+")
                webbrowser.open(f"https://nyaa.si/?f=0&c=0_0&q={title}&s=id&o=desc")


def list_nyaa(user_id):
    user_response = requests.get(APIBASE + f"users/list/{user_id}/today").json()
    return user_response["result"]
