from app import APIBASE, TerminalColor
import requests
import json


def login(args):
    username, password = args.login

    user_response = requests.post(
        APIBASE + "users/account",
        json={"login": {"username": username, "password": password}},
    )

    if user_response.status_code != 404:
        user_id = user_response.json()["id"]
        user_object = json.dumps({"user": {"username": username, "id": user_id}})

        with open("app/user.json", "w") as f:
            f.write(user_object)

    print(TerminalColor.BOLD + user_response.json()["result"] + TerminalColor.END)


def logout(args):
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "user" in json_object:
            username = json_object["user"]["username"]
            with open("app/user.json", "w") as file:
                user_object = json.dumps({})
                file.write(user_object)

                print(
                    TerminalColor.BOLD + f"Logged out of {username}" + TerminalColor.END
                )
        else:
            print(TerminalColor.BOLD + "---Not logged in---" + TerminalColor.END)


def register(args):
    username, password = args.register
    user_response = requests.post(
        APIBASE + "users/account",
        json={"register": {"username": username, "password": password}},
    )

    print(TerminalColor.BOLD + user_response.json()["result"] + TerminalColor.END)
