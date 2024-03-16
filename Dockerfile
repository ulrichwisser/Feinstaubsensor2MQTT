FROM python:3.9 
ADD Feinstaubsensor_WebServer_to_MQTT.py .
ADD config.yaml .
RUN pip install paho-mqtt pyaml-env
CMD ["python","Feinstaubsensor_WebServer_to_MQTT.py"] 

