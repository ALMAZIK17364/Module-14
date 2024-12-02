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

cursor.execute("UPDATE Users SET BALANCE = ? WHERE id % 2 != 0", (500,))

a = 3
for i in range(1, 11):
    if a == 3:
        cursor.execute(f'DELETE FROM USERS WHERE id == {i}')
    a+=1
    if a > 3:
        a = 1





cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
results = cursor.fetchall()

cursor.execute('DELETE FROM Users WHERE id = 6')

cursor.execute("SELECT COUNT(*) FROM Users")
cnt = cursor.fetchone()

cursor.execute("SELECT SUM(balance) FROM Users")
balance_sum = cursor.fetchone()

print(balance_sum[0] / cnt[0])

connection.commit()
connection.close()