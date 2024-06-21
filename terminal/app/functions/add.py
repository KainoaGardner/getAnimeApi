from app import APIBASE, TerminalColor
import requests
import json


def clear(args):
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "user" not in json_object:
            print(TerminalColor.BOLD + "---Not logged in---" + TerminalColor.END)
        else:
            user_id = json_object["user"]["id"]

            result = requests.delete(
                APIBASE + f"users/add/{user_id}/clear",
            )

            print(TerminalColor.BOLD + "---Watchlist cleared---" + TerminalColor.END)


def add(args):
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "user" not in json_object:
            print(TerminalColor.BOLD + "---Not logged in---" + TerminalColor.END)
        else:
            user_id = json_object["user"]["id"]

            shows = args.add
            user_response = requests.post(
                APIBASE + f"users/add/{user_id}/add",
                json={"shows": shows},
            ).json()

            print(TerminalColor.BOLD + "---Added---" + TerminalColor.END)

            for count, anime in enumerate(user_response["added"]):
                print(
                    TerminalColor.BOLD
                    + f"{count + 1} ID: "
                    + anime[1]
                    + TerminalColor.END,
                    end=" ",
                )
                print(anime[0])


def delete(args):
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "user" not in json_object:
            print(TerminalColor.BOLD + "---Not logged in---" + TerminalColor.END)
        else:
            user_id = json_object["user"]["id"]

            shows = args.delete
            result = requests.delete(
                APIBASE + f"users/add/{user_id}/delete", json={"shows": shows}
            ).json()

            print(TerminalColor.BOLD + "---Deleted---" + TerminalColor.END)
            for count, anime in enumerate(result["deleted"]):
                print(
                    TerminalColor.BOLD
                    + f"{count + 1} ID: "
                    + anime[1]
                    + TerminalColor.END,
                    end=" ",
                )
                print(anime[0])
