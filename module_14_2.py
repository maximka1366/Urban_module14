import sqlite3



connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')


cursor.execute('DELETE FROM Users WHERE id = ?', (6,))


cursor.execute('SELECT COUNT(*) FROM Users')
count_ = cursor.fetchone()[0]


cursor.execute('SELECT SUM(balance) FROM Users')
sum_bal = cursor.fetchone()[0]


cursor.execute('SELECT AVG(balance) FROM Users')
avg_ = cursor.fetchone()[0]

print(sum_bal/count_)
print(avg_)



connection.commit()
connection.close()