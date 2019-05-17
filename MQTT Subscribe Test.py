import paho.mqtt.client as mqtt
import DB_Functions as dbf

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("python/test")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    print(dbf.parse_mqtt_payload(str(msg.payload)))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.6.37.100", 1883)

client.loop_forever()
