from acq.scenarios.scenario_base import ScenarioBase


class ScenarioUI(ScenarioBase):
    def __init__(self):
        self.steps = [
            'Login with validation',
            'Create User form validation',
            'Chilling'
        ]
