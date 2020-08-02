import sqlite3

con = sqlite3.connect('userdb.db')

cursor = con.cursor()
cursor.execute("CREATE TABLE Users(Id INTEGER PRIMARY KEY, Name TEXT, Email TEXT, LeavesTaken TEXT, LeavesLeft TEXT)")

con.close()
