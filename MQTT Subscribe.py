import paho.mqtt.client as mqtt
import DB_Functions as dbf
import sqlite3

#connect to database
conn = sqlite3.connect('WeatherData.db')
cursor = conn.cursor()

#create table if it doesn't exist
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

#print database definition
dbf.print_db_definition(cursor, 'readings')

#define new on_connect function
def on_connect(client, userdata, flags, rc):
    #print connection
    print("\nConnected with result code " + str(rc))
    #subscribe to topic
    client.subscribe("sensorData")

#define new on_message function
def on_message(client, userdata, msg):
    #print message
    print('')
    print(msg.topic + " " + str(msg.payload))
    data = dbf.parse_mqtt_payload(str(msg.payload))
    print(data)
    #parse message data
    if(len(data) == 5):
        dbf.make_entry(cursor, data[0], data[1], data[2], data[3], data[4])
        print('data entered')
    else:
        dbf.make_entry(cursor, data[0], data[1], data[2], data[3])
        print('data entered')
    #enter data into database
    dbf.print_latest_entry(cursor, 'readings')

#create new MQTT client object
client = mqtt.Client()
#set function definitions
client.on_connect = on_connect
client.on_message = on_message

#connect to broker
client.connect("10.6.37.100", 1883)
#start loop
client.loop_forever()
