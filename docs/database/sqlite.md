# SQLite

SQLite DB is the database used by the agents and tools. It is used to store the conversations and context messages.

## Initialize SQLite

Create a new SQLite database and tables.

```console
make init-sqlite-db
```

## SQLite Interface

::: director.db.sqlite.db.SQLiteDB
