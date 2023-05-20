import sqlite3


class Users:
    instance = None
    create_users_query = """
        CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
        """

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(Users)
            return cls.instance
        return cls.instance

    def __init__(self, db_name: str):
        self.name = db_name
        self.conn = self.__connect()
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.create_users_query)

    def __connect(self):
        try:
            return sqlite3.connect(self.name)

        except sqlite3.Error as e:
            raise Exception(
                f"An error occured while connecting to the Users. {e}")

    def fetch_users_data(self):
        all_users_info_query = """
            SELECT username, password FROM users
        """

        self.cursor.execute(all_users_info_query)

        result = self.cursor.fetchall()

        return result

    def insert_user(self, username, password):
        insert_user_query = """
                INSERT INTO users (username, password)
                VALUES (?, ?)
            """

        try:
            self.cursor.execute(insert_user_query, (username, password))
            self.conn.commit()

        except sqlite3.Error as e:
            raise Exception(f"An error occured while creating a user. {e}")

    def __del__(self):
        self.cursor.close()
        self.conn.close()
