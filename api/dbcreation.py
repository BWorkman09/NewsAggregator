import sqlite3

with open(r"data\News_Aggregator.db") as sql_file:
    sql_script = sql_file.read()

db = sqlite3.connect('News_Aggregator.db')
cursor = db.cursor()
cursor.executescript(sql_script)
#db.commit()
#db.close()
result = cursor.execute('SELECT * from Article LIMIT 10')
for row in result:
    print(row)
db.close()