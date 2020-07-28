##############################
#                            #
# Author - Aman Kanwar       #
# MQTT example code          #
# Subscriber                 #
#                            #
##############################

# importing the library and creating the instance of the same
import paho.mqtt.client as mqtt
import time


# Taking the variables for the methods
client      =   mqtt.Client()
topicName   =   "phy/test"
QOS_val        =   2

client.username_pw_set(username="phy",password="phyfdsa")

# --------------- Defining call backs---------------------------------------------------------------
def on_connect(pvtClient,userdata,flags,rc):
    if(rc == 0):  # on successful connection
        print("Connected to client! Return Code:"+str(rc)) # printing the data on the screen
        # Once connection is established, subscribe to the topic
        # important, here we are subscribing to a topic only after getting the authentication done
        # further we are setting the QOS in the .subscribe(...) method
        result = client.subscribe(topicName, QOS_val)  # getting the Tuple from the call back

    elif(rc ==5): # in case of authentication error
        print("Authentication Error! Return Code: "+str(rc))  # printing the data on the screen
        client.disconnect()

def write_to_file(data):
  f = open("/usr/src/app/logs/logfiles.txt", "a+")
  f.write(data + "\n")
  f.close()


#           Call back for the message
# This call-back will run whenever there is a message (payload) published on the given topic
def on_message(pvtClient, userdata, msg):
    # here we are extracting details from the msg parameter,
    print("\n============================================")
    print("Payload       : " +str(msg.payload.decode()))
    print("Qos of message: "+str(msg.qos))
    print("Message Topic : "+str(msg.topic))
    print("Message retain: "+ str(msg.retain))
    print("============================================\n")

    write_to_file(msg.payload.decode())

    if(msg.payload.decode() == "exit(0)" ):
        client.disconnect()

'''
# currently not using this callback
def will_set(pvtClient, payload="disconnected!!!", qos=2, retain=False):
    print("status: "+payload)
'''

# this call back is used for the log generation
def on_log(topic, userdata, level, buf):
    print("Logs: "+str(buf))
# -------------------------------------------------------------------------------------------------------------

# ======== Associating the methods with the given callbacks of the MQTT ======
client.on_connect   =   on_connect
client.on_message   =   on_message
client.on_log       =   on_log
#client.will_set     =   will_set
# ============================================================================

host        = "broker"
port        = 1883
keepAlive   = 60

client.connect(host,port,keepAlive) # establishing the connection

time.sleep(2)               # giving a sleep time for the connection to setup

client.loop_forever()