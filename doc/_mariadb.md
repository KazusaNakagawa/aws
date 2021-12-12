## MariaDB CMD

- Connection

```bash
 $ mysql -u<user_name> -p<password> 
```

- Database List
```bash
> show databases;

# OutPut
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
 
```

### USE Database
```bash
> USE <Databese Name>;

# OutPut
MariaDB [mysql]>
```

### show tables;
```bash
MariaDB [mysql]> show tables;

# OutPut
+---------------------------+
| Tables_in_mysql           |
+---------------------------+
| column_stats              |
| columns_priv              |
| db                        |
| event                     |
| func                      |
| general_log               |
| global_priv               |
| gtid_slave_pos            |
| help_category             |
| help_keyword              |
| help_relation             |
| help_topic                |
| index_stats               |
| innodb_index_stats        |
| innodb_table_stats        |
| plugin                    |
| proc                      |
| procs_priv                |
| proxies_priv              |
| roles_mapping             |
| servers                   |
| slow_log                  |
| table_stats               |
| tables_priv               |
| time_zone                 |
| time_zone_leap_second     |
| time_zone_name            |
| time_zone_transition      |
| time_zone_transition_type |
| transaction_registry      |
| user                      |
| users                     |
+---------------------------+
32 rows in set (0.014 sec)

```

### SELECT * FROM [table name];
```bash
MariaDB [mysql]> SELECT * FROM users;

# OutPut
+----+------+--------------+
| id | name | email        |
+----+------+--------------+
|  1 | name | test@com.com |
+----+------+--------------+
1 row in set (0.006 sec)

```