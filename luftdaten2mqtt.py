#!/usr/bin/env python3
# Changed and updated by Ulrich Wisser
#
# forked from https://github.com/StefanHol/Feinstaubsensor_WebServer_to_MQTT
# Written by Stefan Holstein
#
# Luftsensor Daten separiert über mqtt weiterleiten
# Luftsensor -> ThisServer -> MQTTBroker
#
# thanks to Nathan Hamiel (2010)
# # https://gist.github.com/huyng/814831
# and thanks to
# # https://stackoverflow.com/a/30288641/9722867
#

from http.server import HTTPServer, BaseHTTPRequestHandler
# from optparse import OptionParser
import paho.mqtt.client as mqtt
import json
import logging
from logging.handlers import RotatingFileHandler
from pyaml_env import parse_config, BaseConfig

class main():
    def __init__(self):
        config = BaseConfig(parse_config('config.yaml', tag='!ENV'))
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=config.log_level)
        logging.info("luftdaten2mqtt version 0.1.2")
        self.mqttH = mqttHandler(config)
        self.server = myHTTP_2_MQTT_Pushlisher(config, self.mqttH)

class myHTTP_2_MQTT_Pushlisher():
    def __init__(self, config, MQTT):
        try:
            server = HTTPServer((config.http_server.ip, config.http_server.port), RequestHandler)
            server.mqtt = MQTT
            logging.info('Listening HTTP on %s:%s' % (config.http_server.ip, config.http_server.port))
            server.serve_forever()
        except Exception as e:
            logging.error("Error: starting HTTP Server: %s, IP: %s, Port: %s" %(e, config.http_server.ip, config.http_server.port) )
            exit()

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # we do nothing, just return 200 OK
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        request_path = self.path

        request_headers = self.headers
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0

        data = self.rfile.read(length)
        self.server.mqtt.HTTP_2_MQTT(data)

        self.send_response(200)
        self.end_headers()

    do_PUT = do_GET
    do_DELETE = do_GET


class mqttHandler():
    def __init__(self, config):
        self.mqttServer = config.mqtt.server
        self.mqttUserId = config.mqtt.user
        self.mqttPassword = config.mqtt.password
        self.mqttPort = config.mqtt.port

        self.AllowedIDs = config.allowed_sensors
        self.Prefix = config.mqtt.prefix
        self.Topic = config.mqtt.topic

        self.TopicAndPrefix = self.Prefix + "/" + self.Topic
        self.init_mqtt()

    def init_mqtt(self):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        try:
            self.mqttc.username_pw_set(self.mqttUserId, self.mqttPassword)
            self.mqttc.connect(self.mqttServer, self.mqttPort)
            self.mqttc.loop_start()
            logging.info('Connected to MQTT-Broker on %s:%s' % (self.mqttServer, self.mqttPort))
        except Exception as e:
            logging.error("Error: connecting mqtt Server: %s, IP: %s, Port: %s" %(e, self.mqttServer, self.mqttPort) )


    def HTTP_2_MQTT(self, raw_data):
        logging.debug("HTTP_2_MQTT: %s" %(raw_data))
        try:
            # parse json
            data = json.loads(raw_data.decode().replace("'", '"'))
            # prepare topic
            topic = self.TopicAndPrefix + str(data["esp8266id"])
            # prepare data
            data_dict = {
                'id' : data['esp8266id'],
                'sw_version' : data['software_version'],
            }
            for measurement in data['sensordatavalues']:
                if "BME280_pressure" == str(measurement['value_type']):
                    # preassure data of BME280 have to be divided by 100
                    data_dict[measurement['value_type']] = float(measurement['value']) / 100
                else:
                    data_dict[measurement['value_type']] = measurement['value']
            # publish
            logging.info("Publish %s" % topic)
            self.mqttc.publish(topic, json.dumps(data_dict))
        except Exception as e:
            logging.error("error in read_all_data_from_sensor: %s" %(e))


if __name__ == "__main__":
    main()