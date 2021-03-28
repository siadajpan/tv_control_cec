import logging
import os

from mqtt_utils.messages.mqtt_message import MQTTMessage


class TVAction(MQTTMessage):
    def __init__(self, topic: str, command: str):
        super().__init__(topic)
        self.topic: str = topic
        self.method = os.system
        self.command: str = command
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute(self, *args, **kwargs):
        if args[0]:
            raise NotImplementedError('Execution of TVAction with arguments '
                                      'should be overridden')

        self.logger.debug(f'Executing {self.method} with {self.command}')
        self.method(self.command)

    def __repr__(self):
        out = super().__repr__()
        return f"{out}, method: {self.method}, {self.command}"
