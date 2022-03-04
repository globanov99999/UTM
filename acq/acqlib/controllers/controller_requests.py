import requests

from acq.acqcore.acq_utils import timeit, for_all_methods
from acq.acqlib.controllers.contorller_base import ControllerBase
from acq.configuration.conf import TEST_EMAIL, TEST_PWD

AUTH_URL = 'https://accounts.uat.env.acquire.io/'
POSTFIX_API_LOGIN = 'api/v1/login'

JSON_HEADERS = {'Accept': '*/*', 'Content-Type': 'application/json'}
LOGIN_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}


@for_all_methods(timeit)
class ControllerRequests(ControllerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def start(self):
        res = requests.get(url='https://acquire.io/', headers=JSON_HEADERS)
        self.logger.info(res)

    def clean_up(self):
        # no need to clean up here
        pass

    def stop(self):
        del self

    def login_api_validation(self):
        full_url = '{}{}'.format(AUTH_URL, POSTFIX_API_LOGIN)
        self.logger.info('Login API to {}'.format(full_url))

        res = requests.post(url=full_url,
                            json={'email': TEST_EMAIL,
                                  'password': 'BAD_PWD'})
        if 400 == res.status_code:
            self.logger.info('Login with wrong credentials returned 400 as expected')
        else:
            self.logger.error('Login with wrong credentials returned {} instead of 400'.format(res.status_code))

        res = requests.post(url=full_url,
                            json={'email': TEST_EMAIL,
                                  'password': TEST_PWD})
        assert 200 == res.status_code, 'Login returned {} instead of 200'.format(res.status_code)

        if 200 == res.status_code:
            self.logger.info('Login with correct credentials returned 200 as expected')
            code = res.json()['data']['endpoint']['params']['code']
            self.logger.info('Secret:\n{}'.format(code))
        else:
            self.logger.error('Login with correct credentials returned {} instead of 200'.format(res.status_code))

        self.logger.info('Login API validation complete')

    def do_action(self, step):
        # here to modify step to action in future
        action = step
        if action == 'Login API validation':
            self.login_api_validation()
        elif action == 'Create User API validation':
            self.create_user_api_validation()
        else:
            self.logger.warning('Unexpected step: {}'.format(action))

    def create_user_api_validation(self):
        self.logger.info('Method {} is under development'.format('create_user_api_validation'))
