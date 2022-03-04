class ScenarioBase:
    def __init__(self, **kwargs):
        if 'steps' in kwargs:
            self.steps = kwargs['steps']
        else:
            self.steps = []
        if 'mode' in kwargs:
            self.mode = kwargs['mode']
        else:
            self.mode = 'func'
