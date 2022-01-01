from api.models.chinook import Album, BkAlbum, Chinook


def bk_album_mng():
    bk_al = BkAlbum()
    return bk_al.backup_query()


def tran():
    bk_al = BkAlbum()
    return bk_al.truncate_table()


def album_query(bind_):
    al = Album()
    return al.query(bind_=bind_)


def show_table():
    ch = Chinook()
    return ch.query_show_tables()
