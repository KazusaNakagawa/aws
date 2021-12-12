## MariaDB CMD
- Connection database name
  - Use an optional entry for the database name.
```bash
$ mysql -u<user name> -p<password> <database name>;
```

## Log
- CREATE DATABASE <databse name>
```bash
> CREATE DATABASE chinook;
```

- CREATE SCHEMA <database name>; 

```bash
MariaDB [chinook]> CREATE SCHEMA chinnok;
Query OK, 1 row affected (0.005 sec)
```


- [DROP DATABASE]()
```bash
> DROP DATABASE IF EXIDTS test;
```

## Reference
- [A MariaDB Primer](https://mariadb.com/kb/en/a-mariadb-primer/)