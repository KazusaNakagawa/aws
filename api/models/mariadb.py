import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()

_DB_PORT = os.getenv('DB_PORT')
_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')

_TABLE_NAME = 'users'

config = {
    "host": "127.0.0.1",
    "port": _DB_PORT,
    "user": "root",
    "password": _PASSWORD,
    "database": "mysql",
}


class MySQL(object):

    def __init__(self):
        try:
            self.con = mysql.connector.connect(**config)
            self.cur = self.con.cursor()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
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

    query = ms.cur.execute(sql)

    print(query)
    ms.mysql_close()
