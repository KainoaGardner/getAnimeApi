from app import parser, APIBASE, TerminalColor
import requests
import json


args = parser.parse_args()
if args.login:
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

elif args.logout:
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
            print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)


elif args.register:
    username, password = args.register
    user_response = requests.post(
        APIBASE + "users/account",
        json={"register": {"username": username, "password": password}},
    )

    print(TerminalColor.BOLD + user_response.json()["result"] + TerminalColor.END)

elif args.list:
    with open("app/user.json", "r") as f:
        json_object = json.load(f)
        if "user" not in json_object:
            print(TerminalColor.BOLD + "Not logged in" + TerminalColor.END)
        else:
            username = json_object["user"]["username"]
            user_id = json_object["user"]["id"]

            if "today" in args.list or "t" in args.list:
                user_response = requests.get(
                    APIBASE + f"users/list/{user_id}/today"
                ).json()

                print(TerminalColor.BOLD + "---Airing Today---" + TerminalColor.END)
                for count, anime in enumerate(user_response["result"]):
                    print(
                        TerminalColor.BOLD
                        + f"{count + 1} ID: "
                        + anime[1]
                        + TerminalColor.END,
                        end=" ",
                    )
                    print(anime[0])

            elif "watchlist" in args.list or "wl" in args.list:
                user_response = requests.get(
                    APIBASE + f"users/list/{user_id}/watchlist"
                )
                print(
                    TerminalColor.BOLD + "---Watchlist---" + TerminalColor.END,
                )
                for count, anime in enumerate(user_response.json()["data"]):
                    print(
                        TerminalColor.BOLD
                        + f"{count + 1} "
                        + anime[1]
                        + TerminalColor.END,
                        end=" ",
                    )
                    print(anime[0])

            elif "all" in args.list or "a" in args.list:
                print(TerminalColor.BOLD + "---Getting Shows---" + TerminalColor.END)
                user_response = requests.get(APIBASE + f"users/list/{user_id}/all")
                for count, anime in enumerate(user_response.json()["anime"]):
                    print(
                        TerminalColor.BOLD
                        + f"{count + 1} "
                        + anime[1]
                        + TerminalColor.END,
                        end=" ",
                    )
                    print(anime[0])

elif args.clear:
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


elif args.add:
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
            # print(TerminalColor.BOLD + user_response.json() + TerminalColor.END)

elif args.delete:
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
