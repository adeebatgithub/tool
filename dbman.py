###################################################
# DBMan
# Author      : Adeeb
# Version     : 1.0
# Description : sqlite database manager
###################################################

import os
import sqlite3


# =============== Exception Handling ============= #
class TableNotFound(Exception):
    """
    Raise Exception when database not found in the given path
    """
    pass


class ColNotFound(Exception):
    """
    Raise Exception when the given column name not found while accessing database throught column name
    """
    pass


class SizeNotPermitted(Exception):
    """
    Raise Exception whaen the given size is not in the limit of the specified date type
    """
    pass


# ================ Field Date Types ============== #

class Fields:
    """
    Table column data types for creating table
    """

    @staticmethod
    def PrimaryKey(col_name: str = "id"):
        return f"{col_name} INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"

    @staticmethod
    def _check_size(data_type: str, size: int):
        if size < 0:
            raise SizeNotPermitted

        sizes = {
            "CHAR": 255,
            "VARCHAR": 65535,
            "TEXT": 65535,
            "INT": 255,
            "FLOAT": 255,
        }
        if size > sizes[data_type]:
            raise SizeNotPermitted

    @staticmethod
    def _generate_field(data_type: str, size: int, null: bool):
        Fields._check_size(data_type, size)
        field = f"{data_type}"
        if size != 0:
            field += f"({size})"

        if null:
            field += " NOT NULL"

        return field

    @staticmethod
    def CharField(size: int = 0, null: bool = True):
        data_type = "CHAR"
        return Fields._generate_field(data_type, size, null)

    @staticmethod
    def VarCharField(size: int = 0, null: bool = True):
        data_type = "VARCHAR"
        return Fields._generate_field(data_type, size, null)

    @staticmethod
    def TextField(size: int = 0, null: bool = True):
        data_type = "TEXT"
        return Fields._generate_field(data_type, size, null)

    @staticmethod
    def IntField(size: int = 0, null: bool = True):
        data_type = "INT"
        return Fields._generate_field(data_type, size, null)

    @staticmethod
    def FloatField(size: int = 0, null: bool = True):
        data_type = "FLOAT"
        return Fields._generate_field(data_type, size, null)


# ================================================= #

class DBInit:
    """
    CLass which deal with initial processes
    Include common methods
    """
    db_path: str = "database.db"
    table_name: str = None

    def __init__(self):
        if self.db_path is not None:
            self._check_db_path_()

        if self.table_name is not None:
            self._check_table_name_()

    def _check_db_path_(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"DataBase not found: {self.db_path}")

    def _check_table_name_(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        db_data = self._db_read_(query)
        table_names = [x[0] for x in db_data]
        if self.table_name not in table_names:
            raise TableNotFound(f"Table not found: {self.table_name}")

    def _db_read_(self, query: str, params: tuple = ()):
        db = sqlite3.connect(self.db_path)
        cur = db.cursor()
        data = cur.execute(query, params).fetchall()
        cur.close()
        return data

    def _db_write_(self, query: str, params: tuple = ()):
        db = sqlite3.connect(self.db_path)
        cur = db.cursor()
        cur.execute(query, params)
        db.commit()
        cur.close()


class DBRead(DBInit):
    """
    Class which deals with reading data from the data base
    """

    def db_fetch_all(self):
        query = f" SELECT * FROM {self.table_name}"
        query_data = self._db_read_(query)
        return query_data

    def _check_col_name_(self, col_name: str):
        db = sqlite3.connect(self.db_path)
        cur = db.execute(f"SELECT * FROM {self.table_name}")
        col_names = [description[0] for description in cur.description]
        db.close()
        if col_name not in col_names:
            raise ColNotFound(f"column '{col_name}' not found in '{self.table_name}' of '{self.db_path}'")

    @staticmethod
    def _data_to_list_(data: list[tuple]):
        if len(data[0]) == 1:
            return [x[0] for x in data]
        return [x for x in data[0]]

    def db_fetch_col(self, col_name: str):
        self._check_col_name_(col_name)
        query = f"SELECT {col_name} FROM {self.table_name}"
        query_data = self._db_read_(query)
        clean_data = DBRead._data_to_list_(query_data)
        return clean_data

    def db_fetch_row(self, **where):
        col, value = where.popitem()
        query = f"SELECT * FROM {self.table_name} WHERE {col} = ?"
        param = (value,)
        query_data = self._db_read_(query, param)
        clean_data = DBRead._data_to_list_(query_data)
        return clean_data


class DBWrite(DBInit):
    """
    Class which deals with writing data to the data base
    """

    def create_table(self, table: dict[str, dict]):
        """
        Use dbman.Fields for specifying data types
        :param: {"table_name": {"col_name": "data type (dbman.Fields)",...}}
        """
        table_name, table_details_dict = table.popitem()
        table_details = ", ".join([f"{col} {data_type}" for col, data_type in table_details_dict.items()])
        pk_col = Fields.PrimaryKey()
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({pk_col}, {table_details})"
        self._db_write_(query)

    def db_insert(self, col_data: dict):
        cols = ', '.join(col_data.keys())
        values = ', '.join([f"'{value}'" for value in col_data.values()])
        query = f"INSERT INTO {self.table_name} ({cols}) VALUES ({values})"
        self._db_write_(query)


class DBMan(DBRead, DBWrite):
    """
    For inheritance
    """
    pass


# ===================== Testing =================== #

class Test(DBMan):
    pass


if __name__ == "__main__":
    test = Test()
    test.__init__()
