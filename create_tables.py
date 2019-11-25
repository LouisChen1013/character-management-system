import sqlite3

conn = sqlite3.connect('characters.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE characters
          (_id INTEGER PRIMARY KEY ASC, 
           _health INTEGER NOT NULL,
           _damage INTEGER NOT NULL,
           _position STRING NOT NULL,
           _alive INTEGER NOT NULL
           type VARCHAR(7) NOT NULL,
           _monster_ai_difficulty VARCHAR(100),
           _monster_type VARCHAR(100)
           _player_level INTEGER,
           _job VARCHAR(100)
          ''')

conn.commit()
conn.close()
