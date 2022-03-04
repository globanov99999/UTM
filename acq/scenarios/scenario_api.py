from acq.scenarios.scenario_base import ScenarioBase


class ScenarioAPI(ScenarioBase):
    def __init__(self):
        self.steps = [
            'Login API validation',
            'Create User API validation',
            'Chilling'
        ]
