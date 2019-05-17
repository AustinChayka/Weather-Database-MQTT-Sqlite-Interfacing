import sqlite3
import DB_Functions as dbf

conn = sqlite3.connect('WeatherData.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        light_level REAL,
        pressure REAL,
        humidity REAL
    );
''')

dbf.print_db_definition(cursor, 'readings')

for row in cursor.fetchall():
    print(row)

dbf.make_entry(cursor, 67.0, .5, 122.0, .03)

dbf.print_db_entries(cursor, 'readings')

conn.commit()

conn.close()

print('\ndone')
