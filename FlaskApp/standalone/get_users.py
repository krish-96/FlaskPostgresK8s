import sys
import argparse
from pathlib import Path


def get_details():
    parser = argparse.ArgumentParser(prog="PROG", usage="%(prog)s [options]")
    # parser.add_argument("-u", "--username", help="username help")
    parser.print_help()

    args = parser.parse_args()
    # print(f"username ==> {args.username}")

    return args


def get_users():
    username = get_details()

    # setting the path
    path = Path(__file__)
    root_path = str(path.parent.parent.parent)
    print(f"root_path: {root_path}")
    sys.path.extend([root_path])

    from FlaskApp.log_configs import logger
    from FlaskApp.database.handler import UserHandler

    users = UserHandler().get_users()
    if users:
        logger.info("Users:")
        for user in users:
            print(f"{user}")
    else:
        logger.info("No users found!")
    return dict(user=users)


if __name__ == "__main__":
    get_users()
