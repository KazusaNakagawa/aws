from api.models.chinook import Album, BkAlbum, Chinook


def bk_album_mng():
    bk_al = BkAlbum()
    return bk_al.backup_query()


def tran():
    bk_al = BkAlbum()
    return bk_al.truncate_table()


def album_search(bind_):
    al = Album()
    return al.search(bind_=bind_)


def album_search_all_artist_name():
    al = Album()
    return al.select_artist_name()


def album_search_choice_join_artist_name(bind_='test'):
    al = Album()
    return al.search_artist_name(bind_=bind_)


def show_table():
    ch = Chinook()
    return ch.query_show_tables()
