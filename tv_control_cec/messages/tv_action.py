import os


class TVAction:
    def __init__(self, topic: str, command: str, priority=5):
        self.topic: str = topic
        self.method = os.system
        self.command: str = command
        self.priority = priority

    def execute(self, *args, **kwargs):
        if args:
            raise NotImplementedError('Execution of TVAction with arguments '
                                      'should be overridden')

        self.method(self.command)

    def __repr__(self):
        return f"method: {self.method}, {self.command}"
