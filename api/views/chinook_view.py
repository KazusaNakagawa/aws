from api.controllers.chinook_controller import *


def view_show_tables():
    tables = show_table()
    print(f"{'No':<3}|", 'table')
    print('-' * 20)
    for idx, table in enumerate(tables):
        print(f"{idx + 1:<3}|", table[0])


def view_album_title():
    result = input('search Album Title: ')
    searches = album_search(result)

    print('Search results: ', len(searches))

    for idx, search in enumerate(searches):
        print('-' * 20, idx + 1, '-' * 20)
        print(f"{'AlbumId':<10}", search[0])
        print(f"{'Title':<10}", search[1])
        print(f"{'ArtistId' :<10}", search[2])


if __name__ == '__main__':
    view_album_title()
