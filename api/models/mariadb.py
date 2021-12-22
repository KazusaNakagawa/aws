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


def chinook_operate():
    ms = MySQL()
    table_name = input('Please select table name: ')
    ms.select_query(table_name=table_name)
    ms.close()


if __name__ == '__main__':
    # main()
    chinook_operate()
