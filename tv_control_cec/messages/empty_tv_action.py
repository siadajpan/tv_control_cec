import time

from paho.mqtt.client import MQTTMessage

from tv_control_cec.messages.tv_action import TVAction


class EmptyTVAction(MQTTMessage):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass
