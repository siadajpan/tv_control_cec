import time

from tv_control_cec.messages.tv_action import TVAction


class EmptyTVAction(TVAction):
    def __init__(self):
        super().__init__('', '')

    def execute(self):
        pass
