import logging
import os
import queue
from threading import Thread

from singleton_decorator import singleton

from tv_control_cec.messages.empty_tv_action import EmptyTVAction
from tv_control_cec.messages.tv_action import TVAction


@singleton
class TVController(Thread):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._actions_queue = queue.Queue()
        self._stop_thread = False
        self.executing_priority = 0

    def run(self):
        while not self._stop_thread:
            if self._actions_queue.empty():
                self._logger.debug('TV controller waiting for actions')
                self.executing_priority = 0

            tv_action: TVAction = self._actions_queue.get()

            self.executing_priority = tv_action.priority
            tv_action.execute()
        self._logger.debug('Exiting')

    def stop(self):
        self._logger.debug('Stopping')
        self._stop_thread = True
        self._actions_queue.put(EmptyTVAction())

    def tv_standby(self):
        os.system()

    def tv_on(self):
        os.system("echo 'on 0' | cec-client -s -d 1")
