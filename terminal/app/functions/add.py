from app import APIBASE, TerminalColor
import requests
import json


def clear():
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "token" not in json_object:
            print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
        else:
            token = json_object["token"]
            headersAuth = {"Authorization": "Bearer " + token}

            user_response = requests.delete(
                APIBASE + f"users/add/clear", headers=headersAuth
            ).json()

            if user_response:
                print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)

            else:

                print(
                    TerminalColor.BOLD + "---Watchlist cleared---" + TerminalColor.END
                )


def add(args):
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "token" not in json_object:
            print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
        else:
            token = json_object["token"]
            headersAuth = {"Authorization": "Bearer " + token}

            shows = args.add

            print(TerminalColor.BOLD + "---Adding---" + TerminalColor.END)
            user_response = requests.post(
                APIBASE + f"users/add/add",
                json={"shows": shows},
                headers=headersAuth,
            ).json()

            if "msg" in user_response:
                print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)

            else:

                for count, anime in enumerate(user_response):
                    print(
                        TerminalColor.BOLD
                        + f"{count + 1} ID: "
                        + anime
                        + TerminalColor.END,
                        end=" ",
                    )
                    print(user_response[anime]["title"])


def delete(args):
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "token" not in json_object:
            print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
        else:
            token = json_object["token"]
            headersAuth = {"Authorization": "Bearer " + token}
            print(TerminalColor.BOLD + "---Deleting---" + TerminalColor.END)

            shows = args.delete
            user_response = requests.delete(
                APIBASE + f"users/add/delete",
                json={"shows": shows},
                headers=headersAuth,
            ).json()

            if "msg" in user_response:
                print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)

            else:
                for count, anime in enumerate(user_response):
                    print(
                        TerminalColor.BOLD
                        + f"{count + 1} ID: "
                        + anime
                        + TerminalColor.END,
                        end=" ",
                    )
                    print(user_response[anime]["title"])
