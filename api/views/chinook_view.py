from api.controllers.chinook_controller import *


def view_show_tables():
    tables = show_table()
    print(f"{'No':<3}|", 'table')
    print('-' * 20)
    for idx, table in enumerate(tables):
        print(f"{idx + 1:<3}|", table[0])


if __name__ == '__main__':
    view_show_tables()
