from tv_control_cec.settings import settings
from tv_control_cec.messages.tv_action import TVAction


class TVStandby(TVAction):
    def __init__(self):
        super().__init__(topic=settings.Messages.STANDBY,
                         command=settings.OSCommands.STANDBY)
