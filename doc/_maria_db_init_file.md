## Introduction.
Since it was not possible to insert the original data into Doctor, 
it was necessary to insert the target using the direct mount SQL method.

## Prerequisite.
- MariaDB accessed.
- The sql file is already mounted in the target directory.

## Flow

1.Check the target database
```bash
MariaDB [none]> show databases;
+--------------------+
| Database           |
+--------------------+
| Chinook            |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
```

2.Switch to the target database
```bash
MariaDB [none]> use Chinook;
```

3.Insert target file
```bash
MariaDB [Chinook]> source Chinook_MySql.sql;
...
Query OK, 1 row affected (0.000 sec)
Query OK, 1 row affected (0.001 sec)
Query OK, 1 row affected (0.001 sec)
```

4.Check insert data
```bash
MariaDB [Chinook]> show tables;
+-------------------+
| Tables_in_Chinook |
+-------------------+
| Album             |
| Artist            |
| Customer          |
| Employee          |
| Genre             |
| Invoice           |
| InvoiceLine       |
| MediaType         |
| Playlist          |
| PlaylistTrack     |
| Track             |
+-------------------+
11 rows in set (0.007 sec)
```

```bash
MariaDB [Chinook]> select * from Album LIMIT 3;
+---------+---------------------------------------+----------+
| AlbumId | Title                                 | ArtistId |
+---------+---------------------------------------+----------+
|       1 | For Those About To Rock We Salute You |        1 |
|       2 | Balls to the Wall                     |        2 |
|       3 | Restless and Wild                     |        2 |
+---------+---------------------------------------+----------+
3 rows in set (0.008 sec)
```

## postscript
By changing the root username, 
the mounted initial SQL was inserted when Docker was launched.