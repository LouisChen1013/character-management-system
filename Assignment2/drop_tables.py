import sqlite3

conn = sqlite3.connect('characters.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE characters
          ''')

conn.commit()
conn.close()
