import atexit

from acq.acqcore.acq_logger import ACQLogger


class ControllerBase:
    def __init__(self, *args, **kwargs):
        self.logger = ACQLogger().get_logger()
        self.args = args
        self.kwargs = kwargs
        atexit.register(self.stop)

    def start(self):
        raise NotImplementedError

    def do_action(self, step):
        raise NotImplementedError

    def clean_up(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
