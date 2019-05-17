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

data = dbf.parse_mqtt_payload('b|1,2,3,4,5|')

dbf.make_entry(cursor, data[0], data[1], data[2], data[3])

dbf.print_db_entries(cursor, 'readings')

print()

conn.commit()

conn.close()

print('done')
