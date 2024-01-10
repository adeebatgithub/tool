###################################################
# DBMan
# Author      : Adeeb
# Version     : 1.0
# Description : sqlite database manager
###################################################

import os
import sqlite3

from .fields import PrimaryKeyField


# ============== Exception Handling ============= #

class TableNotFoundError(Exception):
    """
    Raise Exception when database not found in the given path
    """
    pass

class TableNameError(Exception):
    """
    Raise Exception when the table name is not allowed
    """
    pass


class ColumnNotFoundError(Exception):
    """
    Raise Exception when the given column name not found while accessing database through column name
    """
    pass


class ColumnNameError(Exception):
    """
    Raise Exception if the name of column is not allowed
    """
    pass


class DataNotFoundError(Exception):
    """
    Raise Exception when the query data is empty
    """
    pass


# =============================================== #

class DBInit:
    """
    - CLass which deal with initial processes
    - Include common methods
    """
    db_path: str = "database.sqlite"
    table_name: str = None

    def __init__(self):
    	
        if self.table_name is not None:
            self._check_table_name_()

    def _get_table_names_(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        db_data = self._db_read_(query)
        sqlite_default_tables = ("sqlite_master", "sqlite_sequence", "sqlite_stat1")
        return (name[0] for name in db_data if name[0] not in sqlite_default_tables)

    def _check_table_name_(self):
        table_names = self._get_table_names_()
        if not table_names:
            return

        if " " in self.table_name:
            raise TableNameError(f"Table name can not containe white spaces")

        if self.table_name.lower() == "table":
            raise TableNameError(f"Table name can not be {self.table_name}")

        if self.table_name not in table_names:
            raise TableNotFoundError(f"Table not found: {self.table_name}\n\t{self.db_path} --> {self.table_name}")

    def _db_read_(self, query: str, params: tuple = ()):
        """
        To read from the database
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            data = cur.execute(query, params).fetchall()
            cur.close()
            return data

    def _db_write_(self, query: str, params: tuple = ()):
        """
        To write into database
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
            cur.close()

    def _get_col_names_(self):
        with sqlite3.connect(self.db_path) as db:
            cur = db.execute(f"SELECT * FROM '{self.table_name}'")
            col_names = (description[0] for description in cur.description)
            return col_names

    def _check_col_name_(self, col_name: str):
        if " " in col_name:
            raise ColumnNameError("Column name con not containe white spaces")
        return True

    def _check_col_exists_(self, col_name: str):
        col_names = self._get_col_names_()
        if col_name not in col_names:
            raise ColumnNotFoundError(f"column not found: '{col_name}' \n\t{self.db_path} --> {self.table_name} --> {self.db_path}")
        return True


class DBRead(DBInit):
    """
    Class which deals with reading data from the database
    """

    @staticmethod
    def _data_to_list_(data: list[tuple]):
        """
        list[tuple(values)] -> tuple(values)
        """
        return [x[0] for x in data]

    def _data_to_dict_(self, data: list[tuple]):
        """
        list[tuple] -> tuple[dict(column_name: value)]
        """
        col_names = self._get_col_names_()
        clean_data = [dict(zip(col_names, col)) for col in data]
        
        return clean_data

    def db_fetch_all(self, order_by: str = None, desc: bool = False):
        query = f" SELECT * FROM {self.table_name}"
        if order_by is not None:
            query += f" ORDER BY {order_by}"
            if desc:
                query += " DESC"
        query_data = self._db_read_(query)
        return self._data_to_dict_(data=query_data)

    def db_fetch_col(self, col_name: str, order_by: str = None, desc: bool = False):
        self._check_col_exists_(col_name)
        query = f"SELECT {col_name} FROM {self.table_name}"
        if order_by is not None:
            query += f" ORDER BY {order_by}"
            if desc:
                query += " DESC"
        query_data = self._db_read_(query)
        return DBRead._data_to_list_(query_data)

    def db_fetch_row(self, order_by: str = None, desc: bool = False, **conditions):
        condition = ", ".join([f"{col}='{value}'" for col, value in conditions.items() if self._check_col_exists_(col)])
        query = f"SELECT * FROM {self.table_name} WHERE {condition}"
        if order_by is not None:
            query += f" ORDER BY {order_by}"
            if desc:
                query += " DESC"
        query_data = self._db_read_(query)
        if not query_data:
            raise DataNotFoundError(f"value not found: database returned empty list \n\t{col} = {value}")
        return self._data_to_dict_(data=query_data)

    def db_fetch_distinct(self, col_name: str, order_by: str = None, desc: bool = False):
        self._check_col_exists_(col_name)
        query = f"SELECT DISTINCT {col_name} FROM {self.table_name}"
        if order_by is not None:
            query += f" ORDER BY {order_by}"
            if desc:
                query += " DESC"
        query_data = self._db_read_(query)
        return self._data_to_list_(query_data)


class DBWrite(DBInit):
    """
    Class which deals with writing data to the database
    """

    def db_create_table(self, col_descriptions: dict[str, dict], pk: bool = True):
        """
        Parameters
        ----------
        col_descriptions  : dict[column name (str): column data type (dbman.Field)]
        pk : (optional) create a primary key column with name 'id'
        """
        col_details = ", ".join([f"'{col_name}' {data_type.get_query()}" for col_name, data_type in col_descriptions.items()])
        if pk:
            pk_col = PrimaryKeyField()
            col_details = f"{pk_col.get_query()}, {col_details}"
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({col_details})"
        self._db_write_(query)

    def db_insert(self, data: dict = None):
        """
        Parameters
        ----------
        data : dict[column name: value]
        """
        cols = ', '.join([f"{col}" for col in data])
        values = ', '.join([f"'{value}'" for value in data.values()])
        query = f"INSERT INTO {self.table_name} ({cols}) VALUES ({values})"
        self._db_write_(query)

    def db_update(self, data: dict, **conditions):
        """
        Parameters
        ----------
        data : dict[column name: value]
        conditions : where condition, it must be a column (column_name = value)
        """
        update = ", ".join([f"{col} = '{value}'" for col, value in data.items()])
        condition = ", ".join(f"{col} = '{value}'" for col, value in conditions.items())
        query = f"UPDATE {self.table_name} SET {update} WHERE {condition}"
        self._db_write_(query)

    def db_delete(self, **conditions):
        """
        Parameters
        ----------
        conditions : where condition, it must be a column (column_name = value)
        """
        condition = ", ".join([f"{col}='{value}'" for col, value in conditions.items()])
        query = f"DELETE FROM {self.table_name} WHERE {condition}"
        self._db_write_(query)

    def db_add_col(self, col_details: dict[str: str]):
        """
        Parameters
        ----------
        col_details : dict[column name(str): data type(dbman.Fields)]
        """
        col_data = " ".join([f"{col_name} {data_type}" for col_name, data_type in col_details.items()])
        query = f"ALTER TABLE {self.table_name} ADD {col_data}"
        self._db_write_(query)

    def db_drop_col(self, col_name: str):
        self._check_col_exists_(col_name)
        query = f"ALTER TABLE {self.table_name} DROP COLUMN {col_name}"
        self._db_write_(query)

    def db_rename_col(self, col_old_name: str, col_new_name: str):
        self._check_col_exists_(col_name=col_old_name)
        query = f"ALTER TABLE {self.table_name} RENAME COLUMN {col_old_name} TO {col_new_name}"
        self._db_write_(query)

    def db_alter_datatype(self, **alter):
        """
        Parameters
        ----------
        alter : (column_name = data_type(dbman.Fields))
        """
        changes = ", ".join([f"{col} {data_type}" for col, data_type in alter.items()])
        query = f"ALTER TABLE {self.table_name} ALTER COLUMN {changes}"
        self._db_write_(query)


class DBMan(DBRead, DBWrite):
    """
    Base class
    """
    pass
