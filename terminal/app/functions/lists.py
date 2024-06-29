from app import APIBASE, TerminalColor

import requests
import webbrowser
import json


def lists(args):
    if "all" not in args.list and "a" not in args.list:
        with open("app/user.json", "r") as f:
            json_object = json.load(f)
            if "token" not in json_object:
                print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
            else:
                token = json_object["token"]
                headersAuth = {"Authorization": "Bearer " + token}

                if "today" in args.list or "t" in args.list:
                    list_today(headersAuth)
                elif "watchlist" in args.list or "wl" in args.list:
                    list_watchlist(headersAuth)
    else:
        list_all()


def list_today(headersAuth):
    print(TerminalColor.BOLD + "---Airing Today---" + TerminalColor.END)
    user_response = requests.get(
        APIBASE + f"users/list/token/today", headers=headersAuth
    ).json()
    if "msg" in user_response:
        print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)

    else:
        for count, anime in enumerate(user_response["result"]):
            print(
                TerminalColor.BOLD + f"{count + 1} ID: " + anime[1] + TerminalColor.END,
                end=" ",
            )
            print(anime[0])


def list_watchlist(headersAuth):
    print(
        TerminalColor.BOLD + "---Watchlist---" + TerminalColor.END,
    )

    user_response = requests.get(
        APIBASE + f"users/list/token/watchlist", headers=headersAuth
    ).json()
    if "msg" in user_response:
        print(TerminalColor.BOLD + "---Not logged in---" + TerminalColor.END)

    else:
        for count, anime in enumerate(user_response["data"]):
            print(
                TerminalColor.BOLD + f"{count + 1} ID: " + anime[1] + TerminalColor.END,
                end=" ",
            )
            print(anime[0])


def list_all():
    print(TerminalColor.BOLD + "---Getting Shows---" + TerminalColor.END)
    user_response = requests.get(APIBASE + f"users/list").json()
    # if "msg" in user_response:
    #     print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
    #
    # else:
    for count, anime in enumerate(user_response):
        print(
            TerminalColor.BOLD + f"{count + 1} ID: " + anime[1] + TerminalColor.END,
            end=" ",
        )
        print(anime[0])


def nyaa():
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "token" not in json_object:
            print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
        else:
            token = json_object["token"]
            headersAuth = {"Authorization": "Bearer " + token}
            print(TerminalColor.BOLD + "---Opened Nyaa Links---" + TerminalColor.END)

            airing_today = list_nyaa(headersAuth)
            if airing_today != "bad":
                for anime in airing_today:
                    title = anime[0].lower()
                    title = title.replace(" ", "+")
                    webbrowser.open(f"https://nyaa.si/?f=0&c=0_0&q={title}&s=id&o=desc")


def list_nyaa(headersAuth):
    user_response = requests.get(
        APIBASE + f"users/list/today", headers=headersAuth
    ).json()
    if "msg" in user_response:
        print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
        return "bad"
    else:
        return user_response["result"]
