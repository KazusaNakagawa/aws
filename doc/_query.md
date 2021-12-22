# Query Doc

## INDEX

1. WHERE
2. INNER JOIN "Album Artist"
3. INSERT INTO ... SELECT

### 1. WHERE
```sql
SELECT * FROM Album WHERE ArtistId = 1;

+---------+---------------------------------------+----------+
| AlbumId | Title                                 | ArtistId |
+---------+---------------------------------------+----------+
|       1 | For Those About To Rock We Salute You |        1 |
|       4 | Let There Be Rock                     |        1 |
+---------+---------------------------------------+----------+
```

### 2. INNER JOIN "Album Artist"
```sql
SELECT Album.ArtistId, Album.Title, Artist.Name
FROM Album
INNER JOIN Artist
ON Album.ArtistId = Artist.ArtistId
ORDER BY Album.ArtistId ASC LIMIT 5;

+----------+---------------------------------------+-----------+
| ArtistId | Title                                 | Name      |
+----------+---------------------------------------+-----------+
|        1 | For Those About To Rock We Salute You | AC/DC     |
|        1 | Let There Be Rock                     | AC/DC     |
|        2 | Balls to the Wall                     | Accept    |
|        2 | Restless and Wild                     | Accept    |
|        3 | Big Ones                              | Aerosmith |
+----------+---------------------------------------+-----------+

```

```sql
SELECT Album.ArtistId, Album.Title, Artist.Name
FROM Album
INNER JOIN Artist
ON Album.ArtistId = Artist.ArtistId
WHERE Artist.ArtistId = 1;

+----------+---------------------------------------+-------+
| ArtistId | Title                                 | Name  |
+----------+---------------------------------------+-------+
|        1 | For Those About To Rock We Salute You | AC/DC |
|        1 | Let There Be Rock                     | AC/DC |
+----------+---------------------------------------+-------+

```

### 3. INSERT INTO ... SELECT

**Flow**
1. Create a table to insert.
2. Insert into a table created from the select source table.
3. result check

**Details**
1. Create a table to insert
Create a backup table for the Album table by adding the columns BK_Data and BK_Number.
```sql
CREATE TABLE IF NOT EXISTS BK_Album (
    `BK_Data` DATETIME NOT NULL,
    `BK_Number` NVARCHAR(30) NOT NULL,
    `AlbumId` INT NOT NULL,
    `Title` NVARCHAR(160) NOT NULL,
    `ArtistId` INT NOT NULL,
    CONSTRAINT `PK_Album` PRIMARY KEY  (`AlbumId`)
);
```

2. Insert into a table created from the select source table.
Execute a query to back up the current Album table with select insert.

**</> SQL file**
```sql
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
```
**</> Python file**
```python
def read_sql_file(self, sql_file, bind_) -> None:
    """ Read the sql file and execute the query.

    :param sql_file: read sql file
    :param bind_: binding variable
    """
    with open(pathlib.Path(f"../../sql/{sql_file}"), 'r') as f:
        sql = f.read()

    self.execute_ex(sql, bind_)
    self.commit()

# >> read sql file
bind_ = [ms.now_time_format(), 'BK-0001']
ms.read_sql_file('bk_album.sql', bind_)
```

3. result check
```sql
SELECT * FROM BK_Album LIMIT 3;
+---------------------+-----------+---------+---------------------------------------+----------+
| BK_Data             | BK_Number | AlbumId | Title                                 | ArtistId |
+---------------------+-----------+---------+---------------------------------------+----------+
| 2021-12-22 22:56:18 | BK-0001   |       1 | For Those About To Rock We Salute You |        1 |
| 2021-12-22 22:56:18 | BK-0001   |       2 | Balls to the Wall                     |        2 |
| 2021-12-22 22:56:18 | BK-0001   |       3 | Restless and Wild                     |        2 |
+---------------------+-----------+---------+---------------------------------------+----------+
```