import datetime
import os
import pathlib
import sys

import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()

_DB_PORT = os.getenv('DB_PORT')
_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
_DATABASE = os.getenv('DATABASE')


class MySQL(object):
    """
    Ref: https://dev.mysql.com/doc/connector-python/en/connector-python-tutorial-cursorbuffered.html

    """

    def __init__(self):
        """ initialization """

        self.config = {
            "host": "127.0.0.1",
            "port": _DB_PORT,
            "user": "root",
            "password": _PASSWORD,
            "database": _DATABASE,
        }

        try:
            self.con = mysql.connector.connect(**self.config)
            self.cur = self.con.cursor()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                sys.exit(1)
            else:
                print('Unknown error')

    def execute(self, sql):
        """ sql query """

        self.cur.execute(
            operation=sql,
        )
        return self.cur.fetchall()

    def execute_ex(self, sql, bind_):
        """ bind sql query """
        try:
            self.cur.execute(
                operation=sql,
                params=bind_
            )

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            self.close()

        return self.cur.fetchall()

    def read_sql_file(self, sql_file, bind_) -> None:
        """ Read the sql file and execute the query.

        :param sql_file: read sql file
        :param bind_: binding variable
        """
        with open(pathlib.Path(f"../../sql/{sql_file}"), 'r') as f:
            sql = f.read()

        self.execute_ex(sql, bind_)
        self.commit()

    def commit(self):
        """ query commit """
        self.con.commit()

    def close(self):
        """ MySQLとの接続を切断する """
        self.cur.close()
        self.con.close()

    def create_table(self, table_name):
        """ Create table default User Table

        columns
        -------
          id, name, email, create_at, update_at

        params
        ------
          table_name(str): table name
        """

        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        sql += "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
        sql += "name VARCHAR(20) NOT NULL, "
        sql += "email VARCHAR(50) NOT NULL, "
        sql += "create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
        sql += "update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
        sql += "CHARSET=utf8mb4"

        self.cur.execute(sql)

    def insert_into_query(self, table_name, *values):

        sql = (
            f"INSERT INTO {table_name} (name, email)"
            "VALUES (%s, %s)"
        )
        data = (values[0], values[1])

        self.cur.execute(
            operation=sql,
            params=data
        )

    def update_query(self, table_name, id_, set_name, email_update):
        """ update query default User Table

        params
        ------
          table_name(str): table name
          id_(int): id
          set_name(str): calum name
          email_update(str): update email

        """

        sql = f"UPDATE {table_name} "
        sql += f"SET name = '{set_name}', "
        sql += f"email = '{email_update}', "
        sql += f"update_at = '{self.now_time_format()}' "
        sql += f"WHERE id = {id_}"

        self.cur.execute(
            operation=sql,
        )

    def select_query(self, table_name):
        """ select query

        params
        ------
          table_name(str): table name
        """

        self.cur.execute(f"SELECT * FROM {table_name}")
        result = self.cur.fetchall()

        for x in result:
            print(x)

    def now_time_format(self):
        """ now datetime format

        :return
          now time
        """
        now = datetime.datetime.now()
        f = '%Y-%m-%d %H:%M:%S'

        return now.strftime(f)


def main():
    print('start ...')

    ms = MySQL()

    ms.update_query(
        table_name='users',
        id_=101,
        set_name='user101',
        email_update="rename22@sample.com",
    )

    ms.create_table("users")

    for i in range(1, 10):
        ms.insert_into_query(
            'users',
            f"user{i}", f"user{i}@test.com",
        )
    ms.commit()
    ms.close()

    print('end ...')


def chinook_operate():
    ms = MySQL()
    table_name = input('Please select table name: ')
    ms.select_query(table_name=table_name)
    ms.close()


if __name__ == '__main__':
    # main()
    chinook_operate()
