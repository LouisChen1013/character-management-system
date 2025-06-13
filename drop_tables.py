import sqlite3

conn = sqlite3.connect("characters.sqlite")

c = conn.cursor()
c.execute(
    """
    DROP TABLE IF EXISTS characters
"""
)

conn.commit()
conn.close()
