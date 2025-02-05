import sqlite3

con = sqlite3.connect('base.db')
cur = con.cursor()
'''cur.execute("""CREATE TABLE visitors(
name VARCHAR(256) NOT NULL,
email TEXT,
message TEXT,
date DATETIME DEFAULT CURRENT_TIMESTAMP
)""")
cur.execute("""SELECT * FROM visitors""")'''
cur.execute("""INSERT INTO users(user_name, password) VALUES('Maksim', 'S898529mr1')""")
con.commit()
print(cur.fetchall())