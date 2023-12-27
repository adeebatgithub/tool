###################################################
# DBMan
# Author      : Adeeb
# Version     : 1.0
# Description : sqlite database manager
###################################################

import os
import sqlite3
from typing import Optional


# ============== Exception Handling ============= #

class TableNotFound(Exception):
    """
    Raise Exception when database not found in the given path
    """
    pass


class ColNotFound(Exception):
    """
    Raise Exception when the given column name not found while accessing database through column name
    """
    pass


class SizeNotPermitted(Exception):
    """
    Raise Exception when the given size is not in the limit of the specified date type
    """
    pass


class DataNotFound(Exception):
    """
    Raise Exception when the query data is empty
    """
    pass


# =============== Field Date Types ============== #

class Fields:
    """
    Sqlite data types

    Common Sqlite data types for specifying while creating table
    """

    @staticmethod
    def PrimaryKey(col_name: str = "id"):
        return f"{col_name} INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"

    @staticmethod
    def ForeignKey(col_name: str, foreign_table: str):
        return f"INTEGER NOT NULL, FOREIGN KEY ('{col_name}') REFERENCES {foreign_table}(id)"

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
    def _generate_field_(data_type: str, size: int, null: bool, unique: bool = False):
        Fields._check_size(data_type, size)
        field = f"{data_type}"
        if size != 0:
            field += f"({size})"

        if null:
            field += " NOT NULL"

        if unique:
            field += " UNIQUE"

        return field

    @staticmethod
    def CharField(size: int = 0, null: bool = True, unique: bool = False):
        data_type = "CHAR"
        return Fields._generate_field_(data_type, size, null, unique)

    @staticmethod
    def VarCharField(size: int = 0, null: bool = True, unique: bool = False):
        data_type = "VARCHAR"
        return Fields._generate_field_(data_type, size, null, unique)

    @staticmethod
    def TextField(size: int = 0, null: bool = True, unique: bool = False):
        data_type = "TEXT"
        return Fields._generate_field_(data_type, size, null, unique)

    @staticmethod
    def IntField(size: int = 0, null: bool = True, unique: bool = False):
        data_type = "INT"
        return Fields._generate_field_(data_type, size, null, unique)

    @staticmethod
    def FloatField(size: int = 0, null: bool = True, unique: bool = False):
        data_type = "FLOAT"
        return Fields._generate_field_(data_type, size, null, unique)


# =============================================== #

class DBInit:
    """
    CLass which deal with initial processes
    Include common methods
    """
    db_path: str = None
    table_name: str = None

    def __init__(self):
        if self.db_path is not None:
            self._check_db_path_()

        if self.table_name is not None:
            self._check_table_name_(self.table_name)

    def _check_db_path_(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"DataBase not found: {self.db_path}")

    def _get_table_names_(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        db_data = self._db_read_(query)
        sqlite_default = ["sqlite_master", "sqlite_sequence", "sqlite_stat1"]
        return [name[0] for name in db_data if name[0] not in sqlite_default]

    def _check_table_name_(self, table_name: str):
        table_names = self._get_table_names_()
        if not table_names:
            return
        if table_name not in table_names:
            raise TableNotFound(f"Table not found: {table_name}")

    def _db_read_(self, query: str, params: tuple = ()):
        """
        To read from the database
        """
        db = sqlite3.connect(self.db_path)
        cur = db.cursor()
        data = cur.execute(query, params).fetchall()
        cur.close()
        return data

    def _db_write_(self, query: str, params: tuple = ()):
        """
        To write into database
        """
        db = sqlite3.connect(self.db_path)
        cur = db.cursor()
        cur.execute(query, params)
        db.commit()
        cur.close()

    def _get_col_name(self):
        db = sqlite3.connect(self.db_path)
        cur = db.execute(f"SELECT * FROM {self.table_name}")
        col_names = [description[0] for description in cur.description]
        db.close()
        return col_names

    def _check_col_name_(self, col_name: str):
        col_names = self._get_col_name()
        if col_name not in col_names:
            raise ColNotFound(f"column '{col_name}' not found in '{self.table_name}' of '{self.db_path}'")


class DBRead(DBInit):
    """
    Class which deals with reading data from the database
    """

    @staticmethod
    def _data_to_list_(data: list[tuple]):
        """
        list[tuple(values)] -> list(values)
        """
        return [x[0] for x in data]

    def _data_to_dict_(self, data: list[tuple]):
        """
        list[tuple] -> dict(column_name: value)
        """
        col_names = self._get_col_name()
        if len(data) == 1:
            return dict(zip(col_names, data[0]))
        clean_data = []
        for col in data:
            clean_data.append(dict(zip(col_names, col)))
        return clean_data

    def db_fetch_all(self, order_by: str = None, desc: bool = False):
        query = f" SELECT * FROM '{self.table_name}'"
        if order_by is not None:
            query += f" ORDER BY '{order_by}'"
            if desc:
                query += " DESC"
        query_data = self._db_read_(query)
        return self._data_to_dict_(data=query_data)

    def db_fetch_col(self, col_name: str, order_by: str = None, desc: bool = False):
        self._check_col_name_(col_name)
        query = f"SELECT '{col_name}' FROM '{self.table_name}'"
        if order_by is not None:
            query += f" ORDER BY '{order_by}'"
            if desc:
                query += " DESC"
        query_data = self._db_read_(query)
        return DBRead._data_to_list_(query_data)

    def db_fetch_row(self, order_by: str = None, desc: bool = False, **where):
        col, value = where.popitem()
        self._check_col_name_(col_name=col)
        query = f"SELECT * FROM '{self.table_name}' WHERE '{col}' = ?"
        if order_by is not None:
            query += f" ORDER BY '{order_by}'"
            if desc:
                query += " DESC"
        param = (value,)
        query_data = self._db_read_(query, param)
        if not query_data:
            raise DataNotFound(f"value not found: {col} = {value}")
        return self._data_to_dict_(data=query_data)

    def db_fetch_distinct(self, col_name: str, order_by: str = None, desc: bool = False):
        self._check_col_name_(col_name)
        query = f"SELECT DISTINCT '{col_name}' FROM '{self.table_name}'"
        if order_by is not None:
            query += f" ORDER BY '{order_by}'"
            if desc:
                query += " DESC"
        query_data = self._db_read_(query)
        return self._data_to_list_(query_data)


class DBWrite(DBInit):
    """
    Class which deals with writing data to the database
    """

    def create_table(self, table_details_dict: dict[str, dict], pk: bool = True):
        """
        Parameters
        ----------
        table_details_dict  : dict[column name (str): column data type (dbman.Field)]
        pk : (optional) create a primary key column with name 'id'
        """
        table_details = ", ".join([f"'{col_name}' {data_type}" for col_name, data_type in table_details_dict.items()])
        if pk:
            pk_col = Fields.PrimaryKey()
            table_details = f"{pk_col}, {table_details}"
        query = f"CREATE TABLE IF NOT EXISTS '{self.table_name}' ({table_details})"
        print(query)
        self._db_write_(query)

    def db_insert(self, col_data: dict = None):
        """
        Parameters
        ----------
        col_data : dict[column name: value]
        """
        cols = ', '.join([f"'{col}'" for col in col_data.keys()])
        values = ', '.join([f"'{value}'" for value in col_data.values()])
        query = f"INSERT INTO '{self.table_name}' ({cols}) VALUES ({values})"
        self._db_write_(query)

    def db_update(self, col_data: dict, **where):
        """
        Parameters
        ----------
        col_data : dict[column name: value]
        where : where condition, it must be a column (column_name = value)
        """
        update = ", ".join([f"'{col}' = '{value}'" for col, value in col_data.items()])
        col_name, value = where.popitem()
        query = f"UPDATE '{self.table_name}' SET {update} WHERE '{col_name}' = ?"
        param = (value,)
        self._db_write_(query, param)

    def db_delete(self, **where):
        """
        Parameters
        ----------
        where : where condition, it must be a column (column_name = value)
        """
        col, value = where.popitem()
        query = f"DELETE FROM '{self.table_name}' WHERE '{col}' = ?"
        param = (value,)
        self._db_write_(query, param)

    def db_add_col(self, col_details: dict[str: str]):
        """
        Parameters
        ----------
        col_details : dict[column name(str): data type(dbman.Fields)]
        """
        col_data = " ".join([f"'{col_name}' {data_type}" for col_name, data_type in col_details.items()])
        query = f"ALTER TABLE '{self.table_name}' ADD {col_data}"
        self._db_write_(query)

    def db_drop_col(self, col_name: str):
        self._check_col_name_(col_name)
        query = f"ALTER TABLE '{self.table_name}' DROP COLUMN '{col_name}'"
        self._db_write_(query)

    def db_rename_col(self, col_old_name: str, col_new_name: str):
        self._check_col_name_(col_name=col_old_name)
        query = f"ALTER TABLE '{self.table_name}' RENAME COLUMN '{col_old_name}' TO '{col_new_name}'"
        self._db_write_(query)

    def db_alter_datatype(self, **alter):
        """
        Parameters
        ----------
        alter : (column_name = data_type(dbman.Fields))
        """
        col_name, data_type = alter.popitem()
        query = f"ALTER TABLE '{self.table_name}' ALTER COLUMN '{col_name}' {data_type}"
        self._db_write_(query)


class DBMan(DBRead, DBWrite):
    """
    Base class
    """
    pass
