import paho.mqtt.client as mqtt
import DB_Functions as dbf
import sqlite3

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

def on_connect(client, userdata, flags, rc):
    print("\nConnected with result code " + str(rc))

    client.subscribe("python/test")

def on_message(client, userdata, msg):
    print('')
    print(msg.topic + " " + str(msg.payload))
    data = dbf.parse_mqtt_payload(str(msg.payload))
    print(data)

    if(len(data) == 5):
        dbf.make_entry(cursor, data[0], data[1], data[2], data[3], data[4])
        print('data entered')
    else:
        dbf.make_entry(cursor, data[0], data[1], data[2], data[3])
        print('data entered')

    dbf.print_db_entries(cursor, 'readings')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.6.37.100", 1883)

client.loop_forever()
