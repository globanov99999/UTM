import atexit


class ActorBase:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        atexit.register(self.stop)

    def start(self):
        raise NotImplementedError

    def clean_up(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
