import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE  IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(1, 11):
    cursor.execute("INSERT INTO Users (id, username, email, age, balance) VALUES (?, ?, ?, ?, ?)",
                   (i, f"User{i}", f"example{i}@gmail.com", i*10, 1000))

cursor.execute("UPDATE Users SET BALANCE = ? WHERE id % 2 = 0", (500,))

cursor.execute('DELETE FROM Users WHERE id % 3 = 1')

cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
results = cursor.fetchall()

connection.commit()
connection.close()