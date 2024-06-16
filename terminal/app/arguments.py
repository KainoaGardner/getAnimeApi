from app import parser

account = parser.add_argument_group("account")
watchlist = parser.add_argument_group("lists")
add_delete = parser.add_argument_group("add_delete")

account.add_argument(
    "-li",
    "--login",
    nargs=2,
    metavar=("username", "password"),
    help="login into account",
)
account.add_argument(
    "-lo", "--logout", action="store_true", help="logout out of account"
)

account.add_argument(
    "-r",
    "--register",
    nargs=2,
    metavar=("username", "password"),
    help="register account",
)

watchlist.add_argument(
    "-l",
    "--list",
    nargs="?",
    const="t",
    type=str,
    choices=["today", "t", "watchlist", "wl", "all", "a"],
    metavar=("type of list"),
    help="list shows in list",
)


add_delete.add_argument(
    "-a",
    "--add",
    nargs="+",
    help="add shows to list by id",
)

add_delete.add_argument(
    "-d",
    "--delete",
    nargs="+",
    help="delete shows from list by id",
)

add_delete.add_argument(
    "-c",
    "--clear",
    action="store_true",
    help="clear all shows in watchlist",
)
