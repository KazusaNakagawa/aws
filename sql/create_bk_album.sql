CREATE TABLE IF NOT EXISTS BK_Album (
    `BK_Data` DATETIME NOT NULL,
    `BK_Number` NVARCHAR(30) NOT NULL,
	`AlbumId` INT NOT NULL,
    `Title` NVARCHAR(160) NOT NULL,
    `ArtistId` INT NOT NULL
);