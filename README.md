# Feinstaubsensor2MQTT

Create simple HTTP Server to receive Data from Sensors (https://luftdaten.info) and Publish these data separated for each value to your MQTT-Broker

Forked from https://github.com/StefanHol/Feinstaubsensor_WebServer_to_MQTT
Original copyright and license are maintained.

This version is meant to be run in  docker container.

# Requirement
- Build your own sensor. See at https://luftdaten.info

# Sensor Configuration
- Log in into your sensor
- enable "Send to own API"
- ![Sensor Configuration](img/SensorConfig.png?raw=true "Sensor Configuration")

# Server Configuration
- modify HTTP Server IP & Port
- modify MQTT Server IP, Port, User & PW
- modify the Topic
- Sensor ID will be a part of the Topic

# Usage
I use this to get my sensor measurements into Homeassistant.

# Home Assistant Config
In the environment variables for the container I did set
``` 
MQTT_PREFIX=Homeassistant
MQTT_TOPIC=Luftdaten/
``` 

In Home Assistant configuration.yaml
``` 
mqtt:
  sensor:
    - name: "LF Temperature"
      unique_id: "ccccccingfhhdtjtejkdurdvlljirevertngglbdhnrb"
      state_topic: "Homeassistant/Luftdaten/<esp8266 id>"
      suggested_display_precision: 1
      unit_of_measurement: "°C"
      value_template: "{{ value_json.BME280_temperature }}"
    - name: "LF Pressure"
      unique_id: "ccccccingfhhcrujgrbccvnettlhhuflfnjgbervbfth"
      state_topic: "Homeassistant/Luftdaten/<esp8266 id>"
      suggested_display_precision: 1
      unit_of_measurement: "hPa"
      value_template: "{{ value_json.BME280_pressure }}"
    - name: "LF Humidity"
      unique_id: "ccccccingfhhntcvvuffiuctnkbgejlfjvtlfijiegbc"
      state_topic: "Homeassistant/Luftdaten/<esp8266 id>"
      suggested_display_precision: 1
      unit_of_measurement: "%"
      value_template: "{{ value_json.BME280_humidity }}"
    - name: "LF PM10"
      unique_id: "ccccccingfhhrifcuvdgegbunnvkljjiblitkdtbuguh"
      state_topic: "Homeassistant/Luftdaten/<esp8266 id>"
      suggested_display_precision: 1
      unit_of_measurement: ""
      value_template: "{{ value_json.SDS_P1 }}"
    - name: "LF PM2.5"
      unique_id: "ccccccingfhhcuvikutellfbcfietbrligrhveggkthn"
      state_topic: "Homeassistant/Luftdaten/<esp8266 id>"
      suggested_display_precision: 1
      unit_of_measurement: ""
      value_template: "{{ value_json.SDS_P2 }}"
```
