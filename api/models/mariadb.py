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


if __name__ == '__main__':
    ms = MySQL()

    sql = """
        CREATE TABLE IF NOT EXISTS {} (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        email VARCHAR(50) NOT NULL
        ) CHARSET=utf8mb4
        """.format(_TABLE_NAME)

    sql_ = """
        INSERT INTO users VALUES(1, 'name', 'test@com.com');
        """

    # query = ms.cur.execute(sql_)

    ms.con.commit()

    # https://dev.mysql.com/doc/connector-python/en/connector-python-tutorial-cursorbuffered.html
    ms.cur.execute("SELECT * FROM users;")

    ms.mysql_close()
