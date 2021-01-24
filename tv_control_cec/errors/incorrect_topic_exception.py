from tv_control_cec.errors.tv_exception import TVException


class IncorrectTopicException(TVException):
    def __init__(self, message):
        super().__init__(message)
