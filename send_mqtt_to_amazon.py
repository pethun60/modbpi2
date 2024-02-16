import paho.mqtt.client as mqtt

# Define callback functions for the first MQTT server
def on_connect_1(client, userdata, flags, rc):
    print("Connected to Server 1 with result code "+str(rc))
    client.subscribe("/temperatur/#")  # Subscribe to a topic on Server 1

def on_message_1(client, userdata, msg):
    # This function will be triggered when a message is received from Server 1
    #message = msg.payload.decode("utf-8")  # Decode the received message
    #message = msg.topic+" value="+str(msg.payload)
    message = msg.topic+" value="+msg.payload.decode("utf-8")
    topic_1 = msg.topic
    print("Received message from Server 1:", message)
    
    # Publish the received message to Server 2
    client_2.publish(topic_1, message)  # Publish the message to Server 2

# Define callback functions for the second MQTT server
def on_connect_2(client, userdata, flags, rc, properties=None):
    print("Connected to Server 2 with result code "+str(rc))

def on_publish_2(client, userdata, mid):
    print("Message published to Server 2")

# Create MQTT client instances for both servers
#client_1 = mqtt.Client()
client_1 = mqtt.Client()
client_1.username_pw_set(username="peter", password="Peter_Th")
# client_2 = mqtt.Client()
client_2 = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)
#client_2.on_connect = on_connect

# enable TLS for secure connection
client_2.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
# set username and password
client_2.username_pw_set("cthunhp", "2RfyNaVkluDZvX")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client_2.connect("639d486d2818424e8c8442808350cfb2.s1.eu.hivemq.cloud", 8883)

# Assign callback functions for Server 1
client_1.on_connect = on_connect_1
client_1.on_message = on_message_1

# Assign callback functions for Server 2
client_2.on_connect = on_connect_2
client_2.on_publish = on_publish_2

# Connect to both MQTT brokers (replace addresses and credentials)
client_1.connect("192.168.1.105", 1883, 60)
client_2.connect("639d486d2818424e8c8442808350cfb2.s1.eu.hivemq.cloud", 8883, 60)

# Start the loop for both clients
client_1.loop_start()
client_2.loop_start()

# Keep the script running to maintain the connection and message transfer
try:
    while True:
        pass
except KeyboardInterrupt:
    client_1.disconnect()
    client_2.disconnect()
    client_1.loop_stop()
    client_2.loop_stop()