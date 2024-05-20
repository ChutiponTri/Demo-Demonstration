import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import streamlit as st
import pandas as pd
import numpy as np
import random
import json

score_order = ["Username", "Game", "Score", "Start", "Finish", "Accuracy"]
overview_order = ["Timestamp", "TimeUsage", "Rotate1", "Dist1", "MeanVel1", "MaxVel1", "Power1", "Rotate2", "Dist2", 
                  "MeanVel2", "MaxVel2", "Power2", "AvgHR", "MaxHR", "Calorie", "Zone"]
raw_data_order = ["Start Time", "Stop Time", "Accel X1", "Accel Y1", "Accel Z1", "Gyro X1", "Gyro Y1", "Gyro Z1", "Raw Dist1", "Raw Vel1"
                "Accel X2", "Accel Y2", "Accel Z2", "Gyro X2", "Gyro Y2", "Gyro Z2", "Heart Rate", "Raw Dist2", "Raw Vel2"]
tabs = ["Demo Graph"]
game = ["Please Select The Game", "AlienInvasion", "BouncingBall", "LuckyBird"]
view = ["Raw Data", "Graph View"]
accel_x = ["Accel X1", "Accel X2"]
accel_y = ["Accel Y1", "Accel Y2"]
accel_z = ["Accel Z1", "Accel Z2"]
gyro_x = ["Gyro X1", "Gyro X2"]
gyro_y = ["Gyro Y1", "Gyro Y2"]
gyro_z = ["Gyro Z1", "Gyro Z2"]
color = ["#0F52BA", "#FF0800"]
max_x = 100
max_rand = 3

ax1_data, ay1_data, az1_data = [], [], []
gx1_data, gy1_data, gz1_data = [], [], []
ax2_data, ay2_data, az2_data = [], [], []
gx2_data, gy2_data, gz2_data = [], [], []

class Stream():
    ax1_data, ay1_data, az1_data = [], [], []
    gx1_data, gy1_data, gz1_data = [], [], []
    ax2_data, ay2_data, az2_data = [], [], []
    gx2_data, gy2_data, gz2_data = [], [], []
    axm_data, aym_data, azm_data = [], [], []
    gxm_data, gym_data, gzm_data = [], [], []
    ชื่อ = ""
    หัวใจ = ""
    def __init__(self):
        # Initialize Config
        st.set_page_config(page_title="Demonstration", page_icon="♿")
        hide_header = """
                    <style>
                    # MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>"""
        st.markdown(hide_header, unsafe_allow_html=True)

        self.broker = MQTT_Server(self)

        # Function To Create Tabs
        self.tab1_ui()
            
    # Function to Create Tab3 UI
    def tab1_ui(self):
        # Username
        self.name_label = st.empty()
        self.update_name("")

        # Header
        st.header("Demonstration 🎬", divider="rainbow")

        col1, col2, col3 = st.columns([0.1, 0.1, 0.8])

        start = col1.button("Start")
        stop = col2.button("Stop")

        self.led_placeholder = st.empty()
        self.update_led(True)

        ข้อความ = "Falling Status : Unknown"
        self.falling_label = st.empty()
        self.falling_label.markdown(f'<div style="display: flex; justify-content: center;">{ข้อความ}</div>',unsafe_allow_html=True)

        # Create Plot
        self.fig, ((self.ax, self.ay, self.az), (self.gx, self.gy, self.gz)) = plt.subplots(2, 3, sharex=True, sharey="row")
        self.line1, = self.ax.plot([], [], "b-")
        self.line2, = self.ay.plot([], [], "b-")
        self.line3, = self.az.plot([], [], "b-")
        self.line4, = self.gx.plot([], [], "b-")
        self.line5, = self.gy.plot([], [], "b-")
        self.line6, = self.gz.plot([], [], "b-")
        self.line7, = self.ax.plot([], [], "r-")
        self.line8, = self.ay.plot([], [], "r-")
        self.line9, = self.az.plot([], [], "r-")
        self.line10, = self.gx.plot([], [], "r-")
        self.line11, = self.gy.plot([], [], "r-")
        self.line12, = self.gz.plot([], [], "r-")
        self.line13, = self.ax.plot([], [], "g-")
        self.line14, = self.ay.plot([], [], "g-")
        self.line15, = self.az.plot([], [], "g-")
        self.line16, = self.gx.plot([], [], "g-")
        self.line17, = self.gy.plot([], [], "g-")
        self.line18, = self.gz.plot([], [], "g-")
        
        # Set Plot X Limit
        self.ax.set_xlim(0, 100)
        self.ay.set_xlim(0, 100)
        self.az.set_xlim(0, 100)
        self.gx.set_xlim(0, 100)
        self.gy.set_xlim(0, 100)
        self.gz.set_xlim(0, 100)

        # Set Plot Y Limit
        self.ax.set_ylim(-3, 3)
        self.ay.set_ylim(-3, 3)
        self.az.set_ylim(-3, 3)
        self.gx.set_ylim(-200, 200)
        self.gy.set_ylim(-200, 200)
        self.gz.set_ylim(-200, 200)

        # Set Plot Title
        self.ax.set_title("Accelerometer X")
        self.ay.set_title("Accelerometer Y")
        self.az.set_title("Accelerometer Z")
        self.gx.set_title("Gyroscope X")
        self.gy.set_title("Gyroscope Y")
        self.gz.set_title("Gyroscope Z")

        self.plot = st.pyplot(self.fig)

        self.hr_label = st.empty()
        
        # Create Animation 
        if start:
            self.broker.start()
            while True:
                if stop:
                    self.broker.stop()
                    break
                self.name_label.markdown(f'<div style="display: flex; justify-content: right; font-size: 24px;">{self.ชื่อ}</div>',unsafe_allow_html=True)
                self.animation_update()
                self.hr_label.markdown(f'<div style="display: flex; justify-content: right; font-size: 24px;">{self.หัวใจ}</div>',unsafe_allow_html=True)
                
    def appendix(self):
        for _ in range(30):
            ax1_data.append(random.uniform(-1.5, 1.5))
            ay1_data.append(random.uniform(-1.5, 1.5))
            az1_data.append(random.uniform(-1.5, 1.5))
            gx1_data.append(random.uniform(-100, 100))
            gy1_data.append(random.uniform(-100, 100))
            gz1_data.append(random.uniform(-100, 100))

    def update_name(self, ชื่อ):
        self.ชื่อ = "User : %s" % ชื่อ

    # Function to update the LED indicator
    def update_led(self, status):
        # if len(self.ax1_data) > 1 and len(self.ax2_data) > 1:
        if status:
            self.led_placeholder.markdown('<div style="display: flex; justify-content: center;"><span style="color:green;font-size:50px">&#x25CF;</span>', unsafe_allow_html=True)
        else:
            self.led_placeholder.markdown('<div style="display: flex; justify-content: center;"><span style="color:red;font-size:50px">&#x25CF;</span>', unsafe_allow_html=True)

    def update1(self, payload):
        self.ax1_data.extend(payload["ax1"])
        self.ay1_data.extend(payload["ay1"])
        self.az1_data.extend(payload["az1"])
        self.gx1_data.extend(payload["gx1"])
        self.gy1_data.extend(payload["gy1"])
        self.gz1_data.extend(payload["gz1"])
    
    def update2(self, payload):
        self.ax2_data.extend(payload["ax2"])
        self.ay2_data.extend(payload["ay2"])
        self.az2_data.extend(payload["az2"])
        self.gx2_data.extend(payload["gx2"])
        self.gy2_data.extend(payload["gy2"])
        self.gz2_data.extend(payload["gz2"])

    def update_m(self, payload):
        self.axm_data.extend(payload["axm"])
        self.aym_data.extend(payload["aym"])
        self.azm_data.extend(payload["azm"])
        self.gxm_data.extend(payload["gxm"])
        self.gym_data.extend(payload["gym"])
        self.gzm_data.extend(payload["gzm"])

    def update_hr(self, payload):
        self.หัวใจ = "Heart Rate : %d" % payload
    
    # Function To Update Plot
    def animation_update(self):
        # print(len(self.ax_data))
        if len(self.ax1_data) > 1:
            self.line1.set_data(range(len(self.ax1_data[-100:])), self.moving_average(self.ax1_data[-100:], 5))
            self.line2.set_data(range(len(self.ay1_data[-100:])), self.moving_average(self.ay1_data[-100:], 5))
            self.line3.set_data(range(len(self.az1_data[-100:])), self.moving_average(self.az1_data[-100:], 5))
            self.line4.set_data(range(len(self.gx1_data[-100:])), self.moving_average(self.gx1_data[-100:], 5))
            self.line5.set_data(range(len(self.gy1_data[-100:])), self.moving_average(self.gy1_data[-100:], 5))
            self.line6.set_data(range(len(self.gz1_data[-100:])), self.moving_average(self.gz1_data[-100:], 5))

            self.line7.set_data(range(len(self.ax2_data[-100:])), self.moving_average(self.ax2_data[-100:], 5))
            self.line8.set_data(range(len(self.ay2_data[-100:])), self.moving_average(self.ay2_data[-100:], 5))
            self.line9.set_data(range(len(self.az2_data[-100:])), self.moving_average(self.az2_data[-100:], 5))
            self.line10.set_data(range(len(self.gx2_data[-100:])), self.moving_average(self.gx2_data[-100:], 5))
            self.line11.set_data(range(len(self.gy2_data[-100:])), self.moving_average(self.gy2_data[-100:], 5))
            self.line12.set_data(range(len(self.gz2_data[-100:])), self.moving_average(self.gz2_data[-100:], 5))

            self.line13.set_data(range(len(self.axm_data[-100:])), self.moving_average(self.axm_data[-100:], 5))
            self.line14.set_data(range(len(self.aym_data[-100:])), self.moving_average(self.aym_data[-100:], 5))
            self.line15.set_data(range(len(self.azm_data[-100:])), self.moving_average(self.azm_data[-100:], 5))
            self.line16.set_data(range(len(self.gxm_data[-100:])), self.moving_average(self.gxm_data[-100:], 5))
            self.line17.set_data(range(len(self.gym_data[-100:])), self.moving_average(self.gym_data[-100:], 5))
            self.line18.set_data(range(len(self.gzm_data[-100:])), self.moving_average(self.gzm_data[-100:], 5))

            if self.az1_data and self.az2_data:
                if (-0.7 < self.az1_data[-1] < 0.7) and (-0.7 < self.az2_data[-1] < 0.7):
                    ข้อความ = "Falling Status : Not Falling"
                    self.falling_label.markdown(f'<div style="display: flex; justify-content: center; font-size: 20px;">{ข้อความ}</div>',unsafe_allow_html=True)
                    self.update_led(True)
                else:
                    ข้อความ = "Falling Status : Falling"
                    self.falling_label.markdown(f'<div style="display: flex; justify-content: center; font-size: 20px;">{ข้อความ}</div>',unsafe_allow_html=True)
                    self.update_led(False)

        self.plot.pyplot(self.fig)

    # Function To calculate Moving Average
    def moving_average(self, data, window_size):
        moving_averages = []
        for i in range(len(data)):
            window = data[max(0, i - window_size + 1):i + 1]
            moving_averages.append(sum(window) / len(window))
        return moving_averages
    
class MQTT_Server():
    def __init__(self, stream):
        self.stream = stream

        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.topic = "ton/server/#"
        broker_address = "broker.hivemq.com"
        broker_port = 1883

        self.client.connect(broker_address, broker_port)

    def start(self):
        self.client.loop_start()
    
    def stop(self):
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected With Result Code {reason_code}")
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg:mqtt.MQTTMessage):
        # print(f"Message {msg.topic} : {msg.payload}")
        message = msg.payload.decode("utf-8")
        payload = json.loads(message)
        if "ax1" in payload.keys():
            self.stream.update1(payload)
        elif "ax2" in payload.keys():
            self.stream.update2(payload)
        elif "axm" in payload.keys():
            self.stream.update_m(payload)
        elif "hr" in payload.keys():
            self.stream.update_hr(payload["hr"])
        elif "name" in payload.keys():
            self.stream.update_name(payload["name"])
        
        
if __name__ == '__main__':
    stream = Stream()
    
