from typing import Optional

from acq.acqcore.acq_logger import ACQLogger
from acq.acqlib.actors.actor_base import ActorBase
from acq.acqlib.controllers.contorller_base import ControllerBase
from acq.acqlib.controllers.controller_requests import ControllerRequests
from acq.scenarios.scenario_base import ScenarioBase

logger = ACQLogger().get_logger()


class ActorWorker(ActorBase):
    def __init__(self, controller: Optional[ControllerBase] = None):
        super(ActorWorker, self).__init__()
        if controller:
            self.controller = controller
        else:
            self.controller = ControllerRequests()

    def start(self):
        self.controller.start()
        logger.info('Worker started')

    def walk_scenario(self, scenario: ScenarioBase):
        for step in scenario.steps:
            self.do_step(step)
        logger.info('Worker walked')

    def do_step(self, step):
        self.controller.do_action(step)
        logger.info('Worker stepped')

    def clean_up(self):
        self.controller.stop()
        self.controller = None

    def stop(self):
        if self.controller:
            self.clean_up()
