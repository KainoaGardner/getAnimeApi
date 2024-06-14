from app import parser

parser.add_argument(
    "-li",
    "--login",
    nargs=2,
    metavar=("username", "password"),
    help="login into account",
)
parser.add_argument(
    "-lo", "--logout", action="store_true", help="logout out of account"
)

parser.add_argument(
    "-r",
    "--register",
    nargs=2,
    metavar=("username", "password"),
    help="register account",
)
