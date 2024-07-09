from app import APIBASE, TerminalColor

import requests
import webbrowser
import json


def lists(args):
    sort_type = get_sort_type(args)
    if "all" not in args.list and "a" not in args.list:
        with open("app/user.json", "r") as f:
            json_object = json.load(f)
            if "token" not in json_object:
                print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
            else:
                token = json_object["token"]
                headersAuth = {"Authorization": "Bearer " + token}

                if "today" in args.list or "t" in args.list:
                    list_today(headersAuth, sort_type)
                elif "watchlist" in args.list or "wl" in args.list:
                    list_watchlist(headersAuth, sort_type)
    else:
        list_all(sort_type)


def list_today(headersAuth, sort_type):
    print(TerminalColor.BOLD + "---Airing Today---" + TerminalColor.END)
    user_response = requests.get(
        APIBASE + f"users/list/token/today", headers=headersAuth
    ).json()

    if "msg" in user_response:
        print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)

    else:
        anime_list = []
        for anime in user_response:
            anime_list.append(
                [
                    anime,
                    user_response[anime]["title"],
                    user_response[anime]["image"],
                    user_response[anime]["ep_count"],
                ]
            )

        anime_list = sort_list(anime_list, sort_type)

        for count, anime in enumerate(anime_list):
            print(
                TerminalColor.BOLD
                + f"{count + 1} ID: "
                + anime[0]
                + " "
                + anime[3]
                + TerminalColor.END,
                end=" ",
            )

            print(anime[1])


def list_watchlist(headersAuth, sort_type):
    print(
        TerminalColor.BOLD + "---Watchlist---" + TerminalColor.END,
    )

    user_response = requests.get(
        APIBASE + f"users/list/token/watchlist", headers=headersAuth
    ).json()
    if "msg" in user_response:
        print(TerminalColor.BOLD + "---Not logged in---" + TerminalColor.END)

    else:
        anime_list = []
        for anime in user_response:
            anime_list.append(
                [
                    anime,
                    user_response[anime]["title"],
                    user_response[anime]["image"],
                ]
            )

        anime_list = sort_list(anime_list, sort_type)

        for count, anime in enumerate(anime_list):
            print(
                TerminalColor.BOLD + f"{count + 1} ID: " + anime[0] + TerminalColor.END,
                end=" ",
            )
            print(anime[1])


def list_all(sort_type):
    print(TerminalColor.BOLD + "---Getting Shows---" + TerminalColor.END)
    user_response = requests.get(APIBASE + f"users/list").json()

    anime_list = []
    for anime in user_response:
        anime_list.append(
            [
                anime,
                user_response[anime]["title"],
                user_response[anime]["image"],
            ]
        )

    anime_list = sort_list(anime_list, sort_type)

    for count, anime in enumerate(anime_list):
        print(
            TerminalColor.BOLD + f"{count + 1} ID: " + anime[0] + TerminalColor.END,
            end=" ",
        )
        print(anime[1])


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
                    title = airing_today[anime]["title"].lower()
                    title = title.replace(" ", "+")
                    webbrowser.open(f"https://nyaa.si/?f=0&c=0_0&q={title}&s=id&o=desc")


def list_nyaa(headersAuth):
    user_response = requests.get(
        APIBASE + f"users/list/token/today", headers=headersAuth
    ).json()
    if "msg" in user_response:
        print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
        return "bad"
    else:
        return user_response


def sort_list(anime_list, sort):
    if sort == "name":
        anime_list.sort(key=lambda x: x[1])
    elif sort == "id":
        anime_list.sort(key=lambda x: x[0])
    else:
        anime_list.reverse()

    sorted_list = anime_list

    return sorted_list


def get_sort_type(args):
    if not args.sort:
        return "recent"
    if "i" in args.sort or "id" in args.sort:
        return "id"
    elif "n" in args.sort or "name" in args.sort:
        return "name"
    else:
        return "recent"
