import sqlite3

con = sqlite3.connect("tasks.db")

cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, Task TEXT, Status TEXT)")