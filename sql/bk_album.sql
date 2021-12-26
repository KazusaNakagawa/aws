INSERT INTO BK_Album (
    BK_Data,
    BK_Number,
    AlbumId,
    Title,
    ArtistId
)
SELECT %s, %s,
    AlbumId,
    Title,
    ArtistId
FROM Album;
