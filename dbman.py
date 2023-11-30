###################################################
# DBMan
# Author      : Adeeb
# Version     : 1.0
# Description : sqlite database manager
###################################################

import sqlite3
import os


class TableNotFound(Exception):
    pass
class ColNotFound(Exception):
    pass

class DBMan:
    db_path: str = "database.db"
    table_name: str = None
    table_names: list = None

    def __init__(self):
        if self.db_path is not None:
            self.get_db_path()

        self.db = sqlite3.connect(self.db_path)
        self.check_table_name()

    def db_execute(self, query: str):
        cur = self.db.cursor()
        data = cur.execute(query).fetchall()
        cur.close()
        return data

    def get_db_path(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError

    def check_table_name(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        db_data = self.db_execute(query)
        table_names = [x[0] for x in db_data]
        if self.table_name not in table_names:
            raise TableNotFound

    def db_fetch_all(self):
        query = f" SELECT * FROM {self.table_name}"
        db_data = self.db_execute(query)
        return db_data

    def check_col_name(self, col: str):
        cur = self.db.execute(f"SELECT * FROM {self.table_name}")
        col_names = [description for description in cur.description]
        if col not in col_names:
            raise ColNotFound

    def db_fetch_col(self, col: str):
        self.check_col_name()
        query = f"SELECT {col} FROM {self.table_name}"
        db_data = self.db_execute(query)
        return db_data

class test(DBMan):

    db_path = "data.db"
    table_name = "Files"

    def __init__(self):
        print("starting...")
        super().__init__()
        self.db_fetch_col(col="bnbnb")

if __name__ == "__main__":
    test()
