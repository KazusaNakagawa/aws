from api.models.chinook import Album, BkAlbum


def bk_album_mng():
    bk_al = BkAlbum()
    # bk_al.create_table()
    # bk_al.truncate_table()
    return bk_al.backup_query()


def tran():
    bk_al = BkAlbum()
    return bk_al.truncate_table()


def album_query():
    al = Album()
    al.query(bind_='a')
