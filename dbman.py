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


class DBInit:
    db_path: str = "database.db"
    table_name: str = None
    table_names: list = None

    def __init__(self):
        if self.db_path is not None:
            self.check_db_path()

        self.db = sqlite3.connect(self.db_path)
        self.check_table_name()

    def check_db_path(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError

    def check_table_name(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        db_data = self.db_read(query)
        table_names = [x[0] for x in db_data]
        if self.table_name not in table_names:
            raise TableNotFound

    def db_read(self, query: str):
        cur = self.db.cursor()
        data = cur.execute(query).fetchall()
        cur.close()
        return data

    def db_write(self, query: str):
        cur = self.db.cursor()
        cur.execute(query)
        cur.close()


class DBRead(DBInit):

    def __init__(self):
        super().__init__()

    def db_fetch_all(self):
        query = f" SELECT * FROM {self.table_name}"
        db_data = self.db_read(query)
        return db_data

    def check_col_name(self, col: str):
        cur = self.db.execute(f"SELECT * FROM {self.table_name}")
        col_names = [description for description in cur.description]
        if col not in col_names:
            raise ColNotFound

    def db_fetch_col(self, col: str):
        self.check_col_name()
        query = f"SELECT {col} FROM {self.table_name}"
        db_data = self.db_read(query)
        return db_data

    def db_fetch_row(self, **where):
        col, value = where.popitem()
        query = f"SELECT * FROM {self.table_name} WHERE {col} = '{value}'"
        db_data = self.db_read(query)
        return db_data


class DBWrite(DBInit):

    def __init__(self):
        super().__init__()

    def create_table(self, null=False, **table):
        table_name, table_details_dict = table.popitem()
        table_details = ", ".join([f"{col} {data_type}" for col, data_type in table_details_dict.items()])
        if null:
            table_details = ", ".join([f"{col} {data_type} NOT NULL" for col, data_type in table_details_dict.items()])
        id_col = "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"
        query = f"CREATE TABLE {table_name} ({id_col}, {table_details}):"
        print(query)


class DBMan(DBRead, DBWrite):

    def __init__(self):
        super().__init__()


class test(DBWrite):
    db_path = "data.db"
    table_name = "Files"

    def __init__(self):
        print("starting...")
        super().__init__()
        self.create_table(null=True, tabel_name={"col_1": "int", "col_2": "str"})


if __name__ == "__main__":
    test()
