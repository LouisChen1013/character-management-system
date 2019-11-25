import sqlite3

conn = sqlite3.connect('characters.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE devices
          ''')

conn.commit()
conn.close()
