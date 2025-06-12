import sqlite3

con = sqlite3.connect("tasks.db")

cursor = con.cursor()

taskname = "mangow"
cursor.execute(f"INSERT INTO tasks (Task, Status) VALUES ('{taskname}', 'Incomplete')")
#print(taskname)
cursor.close()
con.commit()
con.close()

con = sqlite3.connect("tasks.db")

cursor = con.cursor()

#input()
cursor.execute("SELECT * FROM tasks")
result=cursor.fetchall()
print(result)
for row in result:
    print(row)
#cursor.execute(f"SELECT * FROM tasks")

cursor.close()
con.close()