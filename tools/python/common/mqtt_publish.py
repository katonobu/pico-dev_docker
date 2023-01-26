import time
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("hello")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
print("Start try to connect")

client.connect("172.26.32.1", 1883, 60)
#client.connect("public.cloud.shiftr.io", 1883, 60)
#client.connect("34.77.13.55", 1883, 60)

for dummy in range(10):
    time.sleep(1)
    client.publish("hello", payload="{}".format(int(time.time())))
    print("publish")
client.disconnect()

