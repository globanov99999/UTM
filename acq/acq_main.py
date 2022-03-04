"""Main module."""

from acq.acqcore.acq_logger import ACQLogger
from acq.acqcore.acq_utils import timeit
from acq.acqlib.actors.actor_worker import ActorWorker
from acq.acqlib.controllers.controller_requests import ControllerRequests
from acq.acqlib.controllers.controller_selenium import ControllerSelenium
from acq.scenarios.scenario_api import ScenarioAPI
from acq.scenarios.scenario_ui import ScenarioUI

logger = ACQLogger().get_logger()


@timeit
def main():
    logger.info('Lets begin!')
    scenario1 = ScenarioAPI()
    scenario2 = ScenarioUI()

    myactor1 = ActorWorker(ControllerRequests())
    myactor1.start()
    myactor1.walk_scenario(scenario1)
    myactor1.stop()

    myactor2 = ActorWorker(ControllerSelenium())
    myactor2.start()
    myactor2.walk_scenario(scenario2)
    myactor2.stop()

    logger.info('Over and out!')


if __name__ == '__main__':
    main()
