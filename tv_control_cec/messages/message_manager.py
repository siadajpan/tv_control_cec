import logging
from queue import Queue
from threading import Thread
from typing import List, Callable

import paho.mqtt.client as mqtt

from tv_control_cec.errors.incorrect_topic_exception import \
    IncorrectTopicException
from tv_control_cec.errors.tv_exception import TVException

from tv_control_cec.messages.empty_tv_action import EmptyTVAction
from tv_control_cec.messages.tv_action import TVAction
from tv_control_cec.messages.tv_on import TVOn
from tv_control_cec.messages.tv_standby import TVStandby
from tv_control_cec.settings import settings

MESSAGES = [TVOn(), TVStandby()]


class MessageManager(Thread):
    def __init__(self, message_queue: Queue, publish_method: Callable):
        super().__init__()
        self._messages: List[TVAction] = MESSAGES
        self._logger = logging.getLogger(self.__class__.__name__)
        self._topic_registered = [message.topic for message in self._messages]
        self._message_queue = message_queue
        self._publish_method = publish_method
        self._stop_thread = False

    def publish(self, topic, payload):
        self._publish_method(topic, payload)

    def execute_message(self, topic: str, payload: str):
        message = self.check_message(topic)
        try:
            self._logger.debug(f'Executing message {message} with '
                               f'payload {payload}')
            if payload == '':
                payload = None

            message.execute(payload)

        except Exception as ex:
            self._logger.error(f'Error raised during execution of message. '
                               f'Exception: {ex}')
            raise ex

    def check_message(self, topic) -> TVAction:
        self._logger.debug(f'Searching for message topic: {topic}')
        if topic in self._topic_registered:
            return self._messages[self._topic_registered.index(topic)]

        error_message = \
            f'Received message not registered. Registered topics: ' \
            f'{[message.topic for message in self._messages]} got: {topic}'

        self._logger.error(error_message)

        raise IncorrectTopicException(error_message)

    def run(self) -> None:
        while not self._stop_thread:
            message: mqtt.MQTTMessage = self._message_queue.get()
            self._logger.debug(f'Got message topic: {message.topic} '
                               f'payload: {message.payload}')
            try:
                self.execute_message(message.topic, message.payload)
            except TVException as ex:
                self.publish(settings.Mqtt.ERROR_TOPIC, ex.message)
            except Exception as ex:
                self.publish(settings.Mqtt.ERROR_TOPIC, ex)
        self._logger.debug('Exiting')

    def stop(self):
        self._logger.debug('Stopping')
        self._stop_thread = True
        self._message_queue.put(EmptyTVAction())
