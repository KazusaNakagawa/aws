import os
import sys

import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()

_DB_PORT = os.getenv('DB_PORT')
_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')


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
            "database": "mysql",
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

    def mysql_close(self):
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
        self.con.commit()

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

        self.con.commit()

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
        sql += f"email = '{email_update}'"
        sql += f"WHERE id = {id_}"

        self.cur.execute(
            operation=sql,
        )

        self.con.commit()


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

    ms.mysql_close()

    print('end ...')


if __name__ == '__main__':
    main()
