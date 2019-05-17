import sqlite3

def make_entry(cursor, temperature, light_level, pressure, humidity, date = None):
    assert isinstance(temperature, float), 'make_entry(), temperature in not of value float'
    assert isinstance(light_level, float), 'make_entry(), light level in not of value float'
    assert isinstance(pressure, float), 'make_entry(), pressure in not of value float'
    assert isinstance(humidity, float), 'make_entry(), humidity in not of value float'
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

def print_db_definition(cursor, table_name):
    assert isinstance(table_name, str), 'print_db_definition(), table_name is not of value string'
    cursor.execute('PRAGMA table_info(' + table_name + ')')
    print('')
    for row in cursor.fetchall():
        print(row)

def print_db_entries(cursor, table_name):
    assert isinstance(table_name, str), 'print_db_entries(), table_name is not of value string'
    cursor.execute('SELECT * FROM ' + table_name)
    print('')
    for entry in cursor.fetchall():
        print(entry)

def parse_mqtt_payload(payload):
    assert isinstance(payload, str), 'parse_mqtt_payload(), payload is not of type string'
    payload = payload[2:-1]
    output = payload.split(',')
    assert len(output) <= 5, 'parse_mqtt_payload(), payload has too many entries'
    for i in range(len(output)):
        output[i] = float(output[i])
    return output
