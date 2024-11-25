from .connection import get_connection, get_db_details
from .db_helper import execute_query, check_table, execute_ddl_query

from FlaskApp.log_configs import logger

# Module constants
DB_CON_FAILED = "Database Connection Failed"


class SetTestDataBase:
    def __init__(self):
        self.connection = get_connection()

    @staticmethod
    def check_initials(get_con=False):
        connection = get_connection()
        if not connection:
            logger.error(DB_CON_FAILED)
            raise Exception(DB_CON_FAILED)
        if get_con:
            return connection

    def set_test_tables(self):
        try:
            self.check_initials()
            db_name = None
            db_details = get_db_details()
            if db_details and "name" in db_details:
                db_name = db_details["name"]
            logger.info(f"Connected to the PostgreSQL database '{db_name}' successfully!")

            if check_table("select * from test_table;"):
                logger.info("Database Tables are already available!")
                return True

            # Test query: Create a table (if it doesn't exist)
            execute_ddl_query("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100)
                );
            """)
            logger.info("Test table created successfully (if it didn't already exist).")
        except Exception as set_table_err:
            logger.error(f"Exception occurred while setting the tables, Exception: {set_table_err}")

    def set_test_data(self):
        try:
            self.check_initials()
            logger.info("Inserting test data into 'test_table'")
            # Insert test data
            execute_ddl_query("""
                INSERT INTO test_table (name) VALUES (%s)
            """), ("Test Entry",)
            logger.info("Inserted test data into 'test_table'")
        except Exception as set_table_err:
            logger.error(f"Exception occurred while setting the tables data, Exception: {set_table_err}")

    def verify_test_data(self):
        try:
            self.check_initials()
            logger.info("Fetching test data")
            # Insert test data
            result = execute_query("SELECT * FROM test_table")
            logger.info(f"Fetched test data: {result}")
        except Exception as set_table_err:
            logger.error(f"Exception occurred while setting the tables data, Exception: {set_table_err}")
