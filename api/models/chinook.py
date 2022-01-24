import mysql.connector

from api.models.mariadb import MariaDB
from api.models.chinook_sql import SELECT_ARTIST_NAME, SEARCH_ARTIST_NAME


class Chinook(MariaDB):

    def __init__(self):
        super().__init__()

    def query_show_tables(self):
        """ show tables"""
        try:
            sql = 'show tables;'
            result = self.execute(sql)
            self.close()

            return result

        except mysql.connector.Error as e:
            print(e)
            self.close()
            raise mysql.connector.Error


class Album(MariaDB):

    def __init__(self):
        super().__init__()

    def search(self, table='Album', col1='Title', bind_=None):
        """

        :param
          table(str): table name
          col1(str):  column name
          bind_(list): bind var

        :return
          query result
        """
        try:
            sql = f"SELECT * FROM {table} WHERE {col1} LIKE CONCAT('%', %s, '%');"
            result = self.execute_ex(sql, [bind_])
            self.close()

            return result

        except mysql.connector.Error as e:
            print(e)
            self.close()
            raise mysql.connector.Error

    def search_artist_name(self, col1='Album.Title', bind_=None):
        """ select Artist Name"""
        try:
            sql = SEARCH_ARTIST_NAME.format(col1)
            result = self.execute_ex(sql, [bind_])
            self.close()

            return result

        except mysql.connector.Error as e:
            print(e)
            self.close()
            raise mysql.connector.Error

    def select_artist_name(self):
        """ select Artist Name"""
        try:
            result = self.execute(SELECT_ARTIST_NAME)
            self.close()

            return result

        except mysql.connector.Error as e:
            print(e)
            self.close()
            raise mysql.connector.Error


class BkAlbum(MariaDB):

    def __init__(self):
        super().__init__()

    def create_table(self):
        self.read_sql_file('create_bk_album.sql', bind_=[])

    def truncate_table(self, table_name='BK_Album'):
        self.execute(f"TRUNCATE TABLE {table_name};")

        return f"Truncate {table_name}."

    def backup_query(self, bk_num='BK-0001'):
        # read sql file
        bind_ = [self.now_time_format(), bk_num]
        self.read_sql_file('bk_album.sql', bind_)
        self.close()

        return 'backup success!'
