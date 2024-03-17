FROM python:3.9 
ADD luftdaten2mqtt.py .
ADD config.yaml .
RUN pip install paho-mqtt pyaml-env
CMD ["python","luftdaten2mqtt.py"] 
EXPOSE 80/tcp
ENV HTTP_IP 0.0.0.0
ENV HTTP_PORT 80
ENV MQTT_SERVER 127.0.0.1
ENV MQTT_PORT 1883
ENV MQTT_USER ""
ENV MQTT_PASSWD ""
ENV MQTT_PREFIX Homeassistant
ENV MQTT_TOPIC Luftdaten
ENV LOG_LEVEL DEBUG