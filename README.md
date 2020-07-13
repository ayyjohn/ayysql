I'm going to implement my own sqliteDB

spec
* I'm going to have a REPL, start-able by a command
* I'm going to be able to initialize a DB into a local file
* I'm going to be able to instantiate a table with columns that have names and can store strings and ints (for now)
* I'm going to be able to run insert statements that take a table and a dictionary 
** if the correct number of columns are given it will create an entry
** if an incorrect number of columns or values are given or one of the values types is incorrect it will return an error
* I'm going to be able to run select statements that allow you to specify any number of fields and values to match exactly 
* I'm going to be able to run select statements that allow you to specify any number of fields and values to be "like"