from tv_control_cec.errors.tv_exception import TVException


class IncorrectPayloadException(TVException):
    def __init__(self, message):
        super().__init__(message)
