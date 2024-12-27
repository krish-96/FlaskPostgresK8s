import sys
import argparse
from pathlib import Path



def get_details():
    parser = argparse.ArgumentParser(prog="PROG", usage="%(prog)s [options]")
    parser.add_argument("-u", "--username", help="username help")
    parser.print_help()

    args = parser.parse_args()
    print(f"username ==> {args.username}")

    return args.username


def create_user():
    username = get_details()

    # setting the path
    path = Path(__file__)
    root_path = str(path.parent.parent.parent)
    print(f"root_path: {root_path}")
    sys.path.extend([root_path])

    from FlaskApp.log_configs import logger
    from FlaskApp.database.handler import UserHandler
    from FlaskApp.database import get_connection

    print(f"get_connection: {get_connection()}")


    logger.debug(f"Received username from request: {username}")
    user_handler_obj = UserHandler()
    user_handler_obj.create_user(username=username)
    users = user_handler_obj.get_users()
    user_details = {}
    if users:
        for user in users[-1::]:
            if user.get("name") == username:
                user_details = user
                break
    logger.info(f"Create user details: {user_details}")
    return dict(user=user_details)


if __name__ == "__main__":
    create_user()
