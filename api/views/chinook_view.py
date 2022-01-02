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

    if searches:
        for idx, search in enumerate(searches):
            print('-' * 20, idx+1, '-' * 20)
            print(f"{'AlbumId':<10}", search[0])
            print(f"{'Title':<10}", search[1])
            print(f"{'ArtistId' :<10}", search[2])


def view_album_search_artist_name():
    searches = album_search_all_artist_name()

    print('Search results: ', len(searches))

    if searches:
        view_format(searches)


def view_album_search_choice_artist_name():
    result = input('search Album Title: ')
    searches = album_search_choice_join_artist_name(result)

    print('Search results: ', len(searches))

    if searches:
        view_format(searches)


def view_format(searches):
    """ Display format of search results """

    for idx, search in enumerate(searches):
        print('-' * 20, idx+1, '-' * 20)
        print(f"{'AlbumId':<13}", search[0])
        print(f"{'Title':<13}", search[1])
        print(f"{'Artist Name' :<13}", search[2])


if __name__ == '__main__':
    # view_album_title()
    # view_album_search_artist_name()
    view_album_search_choice_artist_name()
