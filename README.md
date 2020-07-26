I'm going to implement my own sqliteDB

spec
* I'm going to have a REPL, start-able by a command, eg `ayysql {filename}`
* I'm going to be able to exit that REPL using `.exit`
* I'm going to support `insert` and `select` statements
* For now it will be a single, hard-coded table with 3 columns
** (id: int, username: varchar(32), and email(varchar255))
* insert statements will look like `insert 1 alec alec@ayyjohn.com`
* select will select all rows from the table
* data will be persisted between runs