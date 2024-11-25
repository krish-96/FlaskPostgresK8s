import os
import psycopg2


def get_db_details():
    try:
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASS')
        return dict(host=host, port=port, name=db_name, user=user, password=password)

    except Exception as db_details_err:
        print(f"Exception occurred while fetching the DB details, Exception: {db_details_err}")


def get_connection():
    try:
        db_details = get_db_details()
        if not db_details:
            raise Exception("Missing DB details!")
        host = db_details.get('host')
        port = db_details.get('port')
        db_name = db_details.get('name')
        user = db_details.get('user')
        password = db_details.get('password')
        return psycopg2.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
    except Exception as con_err:
        print(f"Exception occurred while fetching the DB connection, Exception: {con_err}")
