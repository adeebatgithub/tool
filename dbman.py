###################################################
# DBMan
# Author      : Adeeb
# Version     : 1.0
# Description : sqlite database manager
###################################################

import os
import sqlite3


# Exception handling
class TableNotFound(Exception):
    pass


class ColNotFound(Exception):
    pass

class SizeNotPermitted(Exception):
    pass


class DBInit:
    db_path: str = "database.db"
    table_name: str = None

    def __init__(self):
        if self.db_path is not None:
            self.check_db_path()

        if self.table_name is not None:
            self.check_table_name()

    def check_db_path(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError

    def check_table_name(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        db_data = self.db_read(query)
        table_names = [x[0] for x in db_data]
        if self.table_name not in table_names:
            raise TableNotFound

    # problem: sql injection
    # solution: add parameter for variables such as for WHERE statement
    def db_read(self, query: str):
        db = sqlite3.connect(self.db_path)
        cur = db.cursor()
        data = cur.execute(query).fetchall()
        cur.close()
        return data

    def db_write(self, query: str):
        db = sqlite3.connect(self.db_path)
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        cur.close()


class DBRead(DBInit):

    def db_fetch_all(self):
        query = f" SELECT * FROM {self.table_name}"
        db_data = self.db_read(query)
        return db_data

    def check_col_name(self, col: str):
        db = sqlite3.connect(self.db_path)
        cur = db.execute(f"SELECT * FROM {self.table_name}")
        col_names = [description[0] for description in cur.description]
        db.close()
        if col not in col_names:
            raise ColNotFound

    def db_fetch_col(self, col: str):
        self.check_col_name(col)
        query = f"SELECT {col} FROM {self.table_name}"
        db_data = self.db_read(query)
        return db_data

    def db_fetch_row(self, **where):
        col, value = where.popitem()
        query = f"SELECT * FROM {self.table_name} WHERE {col} = '{value}'"
        db_data = self.db_read(query)
        return db_data


class DBWrite(DBInit):

    def create_table(self, table: dict[str, dict]):
        table_name, table_details_dict = table.popitem()
        table_details = ", ".join([f"{col} {data_type}" for col, data_type in table_details_dict.items()])

        id_col = Fields.PrimaryKey()
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({id_col}, {table_details})"
        print(query)
        self.db_write(query)

    def db_insert(self, col_data: dict):
        cols = ', '.join(col_data.keys())
        values = ', '.join([f"'{value}'" for value in col_data.values()])
        query = f"INSERT INTO {self.table_name} ({cols}) VALUES ({values})"
        self.db_write(query)


class DBMan(DBRead, DBWrite):
    pass

############ FIELDS ############

class Fields:
    
    def PrimaryKey():
        return "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"
        
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
    
    def _generate_field(data_type: str, size: int, null: bool):
        Fields._check_size(data_type, size)
        field = f"{data_type}"
        if size != 0:
            field += f"({size})"
            
        if null:
            field += " NOT NULL"
            
        return field
    
    def CharField(size: int = 0, null: bool = True):
        data_type = "CHAR"
        return Fields._generate_field(data_type, size, null)
        
    def VarCharField(size: int = 0, null: bool = True):
        data_type = "VARCHAR"
        return Fields._generate_field(data_type, size, null)
        
    def TextField(size: int = 0, null: bool =True):
        data_type = "TEXT"
        return Fields._generate_field(data_type, size, null)
        
    def IntField(size: int = 0, null: bool = True):
        data_type = "INT"
        return Fields._generate_field(data_type, size, null)
        
    def FloatField(size: int = 0, null: bool = True):
        data_type = "FLOAT"
        return Fields._generate_field(data_type, size, null)
        
    
