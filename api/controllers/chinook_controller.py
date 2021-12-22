import mysql.connector

from api.models.mariadb import MySQL


def query(table, col1, bind_):
    """

    :param
      table(str): table name
      col1(str):  column name
      bind_(list): bind var

    :return
      query result
    """
    try:
        ms = MySQL()
        sql = f"SELECT * FROM {table} WHERE {col1} LIKE CONCAT('%', %s, '%')"
        result = ms.execute_ex(sql, bind_)
        ms.close()

        return result

    except mysql.connector.Error as e:
        print(e)


def query_bind2(table, col1, bind_):
    """

   :param
      table(str): table name
      col1(str):  column name
      bind_(list): bind var

    :return
      query result
    """
    try:
        ms = MySQL()
        sql = f"SELECT * FROM {table} WHERE {col1} LIKE CONCAT('%', %s, '%') AND ArtistId = %s"
        result = ms.execute_ex(sql, bind_)
        ms.close()

        return result

    except mysql.connector.Error as e:
        print(e)


def pprint():
    print(f"{' ' * 10}  ︎{'*  ' * 3}")


def test1():
    rt = query(table='Album', col1='Title', bind_=['Led'])
    for r in rt:
        print(r)
    pprint()

    rt = query_bind2(table='Album', col1='Title', bind_=['Led', 22])
    for r in rt:
        print(r)


def test2():
    ms = MySQL()

    ms.read_sql_file('create_bk_album.sql', bind_=[])
    a = ms.execute("TRUNCATE TABLE BK_Album;")

    # sql file
    bind_ = [ms.now_time_format(), 'BK-0001']
    ms.read_sql_file('bk_album.sql', bind_)

    ms.select_query('BK_Album LIMIT 3')
    ms.close()


if __name__ == '__main__':
    test2()
