SELECT_ARTIST_NAME = 'SELECT Album.ArtistId, Album.Title, Artist.Name ' \
                     'FROM Album ' \
                     'INNER JOIN Artist ' \
                     'ON Album.ArtistId = Artist.ArtistId ' \
                     'ORDER BY Album.ArtistId;'

SEARCH_ARTIST_NAME = 'SELECT Album.ArtistId, Album.Title, Artist.Name ' \
                     'FROM Album ' \
                     'INNER JOIN Artist ' \
                     'ON Album.ArtistId = Artist.ArtistId ' \
                     "WHERE {} LIKE CONCAT('%', %s, '%')" \
                     'ORDER BY Album.ArtistId;'
