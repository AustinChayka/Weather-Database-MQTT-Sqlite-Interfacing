import sqlite3

#   make_entry(cursor, temperature, light_level, pressure, humidity, date = None)
#       cursor - SQLite3 cursor object
#       temperature - temperature reading as float
#       light_level - light reading as float
#       pressure - pressure reading as float
#       humidity - humidity reading as float
#       (optional) date - reading date as string
#   function makes entry into the database that the cursor is connected to    
def make_entry(cursor, temperature, light_level, pressure, humidity, date = None):
    #check values
    assert isinstance(temperature, float), 'make_entry(), temperature in not of value float'
    assert isinstance(light_level, float), 'make_entry(), light level in not of value float'
    assert isinstance(pressure, float), 'make_entry(), pressure in not of value float'
    assert isinstance(humidity, float), 'make_entry(), humidity in not of value float'
    #check if date value entered and enter data
    if date is not None:
        values = date + ',' + str(temperature) + ',' + str(light_level) + ',' + str(pressure) + ',' + str(humidity)
        print('\n' + values)
        cursor.execute('''
            INSERT INTO readings(date, temperature, light_level, pressure, humidity)''' +
            'VALUES(' + values + ')'
        )
    else:
        values = str(temperature) + ',' + str(light_level) + ',' + str(pressure) + ',' + str(humidity)
        cursor.execute('''
            INSERT INTO readings(temperature, light_level, pressure, humidity)''' +
            'VALUES(' + values + ')'
        )
        print('\n' + 'CURRENT_TIMESTAMP,' + values)

#   print_db_definition(cursor, table_name)
#       cursor - SQLite3 cursor object
#       table_name - string name of table
#   prints the table definition
def print_db_definition(cursor, table_name):
    #check table_name
    assert isinstance(table_name, str), 'print_db_definition(), table_name is not of value string'
    #get table info
    cursor.execute('PRAGMA table_info(' + table_name + ')')
    #print
    print('')
    for row in cursor.fetchall():
        print(row)

#   print_db_entries(cursor, table_name)
#       cursor - SQLite3 cursor object
#       table_name - string name of table
#   prints all database entries
def print_db_entries(cursor, table_name):
    #check table_name
    assert isinstance(table_name, str), 'print_db_entries(), table_name is not of value string'
    #get entries
    cursor.execute('SELECT * FROM ' + table_name)
    #print
    print('')
    for entry in cursor.fetchall():
        print(entry)

#   parse_mqtt_payload(payload)
#       payload - MQTT message payload string
#   parses the message payload into data list
def parse_mqtt_payload(payload):
    #check payload
    assert isinstance(payload, str), 'parse_mqtt_payload(), payload is not of type string'
    #cut padding
    payload = payload[2:-1]
    #split into array
    output = payload.split(',')
    #check number of data entries
    assert len(output) <= 5, 'parse_mqtt_payload(), payload has too many entries'
    #convert values
    for i in range(len(output)):
        if(i != 5):
            output[i] = float(output[i])
    return output

#   print_latest_entry(cursor, table_name)
#       cursor - SQLite3 cursor object
#   prints the newest database entry
def print_latest_entry(cursor, table_name):
    #check table_name
    assert isinstance(table_name, str), 'print_latest_entry(), table_name is not of type string'
    #get data
    cursor.execute('SELECT * FROM ' + table_name + ' WHERE id = (SELECT MAX(id) FROM ' + table_name + ')')
    #print
    print(cursor.fetchall()[0])
