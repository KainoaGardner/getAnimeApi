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
        user_object = json.dumps(user_response.json())

        with open("app/user.json", "w") as f:
            f.write(user_object)

        print(TerminalColor.BOLD + f"Logged into {username}" + TerminalColor.END)
    else:
        print(TerminalColor.BOLD + f"Incorrect information" + TerminalColor.END)


def user():
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "token" not in json_object:
            print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
        else:
            token = json_object["token"]
            headersAuth = {"Authorization": "Bearer " + token}
            user_response = requests.get(
                APIBASE + f"users/list/user", headers=headersAuth
            ).json()
            print(
                TerminalColor.BOLD + f"Logged in as {user_response}" + TerminalColor.END
            )


def logout():
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "token" in json_object:
            with open("app/user.json", "w") as file:
                user_object = json.dumps({})
                file.write(user_object)

                print(TerminalColor.BOLD + f"Logged out" + TerminalColor.END)
        else:
            print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)


def register(args):
    username, password = args.register
    user_response = requests.post(
        APIBASE + "users/account",
        json={"register": {"username": username, "password": password}},
    ).json()

    print(TerminalColor.BOLD + user_response["result"] + TerminalColor.END)


def delete_account(args):
    username, password = args.removeaccount
    user_response = requests.delete(
        APIBASE + "users/account",
        json={"delete": {"username": username, "password": password}},
    )

    print(TerminalColor.BOLD + user_response.json()["result"] + TerminalColor.END)
