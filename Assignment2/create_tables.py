import sqlite3

conn = sqlite3.connect('characters.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE characters
          (id INTEGER PRIMARY KEY ASC, 
           health INTEGER NOT NULL,
           damage INTEGER NOT NULL,
           x INTEGER NOT NULL,
           y INTEGER NOT NULL,
           alive INTEGER NOT NULL,
           type VARCHAR(7) NOT NULL,
           monster_ai_difficulty VARCHAR(100),
           monster_type VARCHAR(100),
           player_level INTEGER,
           job VARCHAR(100))
          ''')

conn.commit()
conn.close()
