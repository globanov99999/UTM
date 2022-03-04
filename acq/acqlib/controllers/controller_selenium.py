import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from acq.acqcore.acq_logger import ACQLogger
from acq.acqcore.acq_utils import timeit, for_all_methods
from acq.acqlib.controllers.contorller_base import ControllerBase
from acq.configuration.conf import TEST_ACCOUNT, TEST_EMAIL, TEST_PWD

TEST_BASE_URL = 'https://{}.uat.env.acquire.io/'.format(TEST_ACCOUNT)
POSTFIX_USERS = 'settings/users'

XPATH_LOGIN_BUTTON = '//button[text()="Log In"]'
LOGIN_ALERTS = ("Please enter a username or email address.", "Don't forget to enter your password.")
CREATE_USER_ALERTS_1 = (
    'Unfortunately, you can’t leave this blank.', 'Unfortunately, you can’t leave this blank.', '', '',  # NOSONAR
    'Password must contain at least 1 lower case,1 upper case,1 number & 1 special character.',
    'Password must contain at least 1 lower case,1 upper case,1 number & 1 special character.',
    '', '', 'Please assign any role', '', '')

CREATE_USER_ALERTS_2 = (
    'Name at least 3 characters long', 'Please enter a valid email address', '', '',
    'Confirm Password does not match ',
    'Confirm Password does not match ',
    '', '', '', '', '')


@for_all_methods(timeit)
class ControllerSelenium(ControllerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.driver = webdriver.Safari()

    def start(self):
        self.driver.get('https://acquire.io/')

    def clean_up(self):
        self.driver.close()
        self.driver = None

    def stop(self):
        if self.driver:
            self.clean_up()

    def screenshot(self):
        pic_name = '{}{}{}'.format(ACQLogger().get_log_file_name(),
                                   time.strftime('%y%m%d_%H%M%S', time.localtime()), '.png')
        self.driver.save_screenshot(pic_name)
        self.logger.info(pic_name)

    def do_action(self, step):
        # here to modify step to action in future
        action = step
        if action == 'Login':
            self.login()
        elif action == 'Login with validation':
            self.login_with_validation()
        elif action == 'Create User form validation':
            self.create_user_form_validation()
        else:
            self.logger.warning('Unexpected step: {}'.format(action))

    def login(self):
        self.logger.info('Login to {}'.format(TEST_BASE_URL))
        self.driver.get(TEST_BASE_URL)
        email_field = WebDriverWait(self.driver, 30).until(lambda d: d.find_element(value='usernameOrEmail'))
        email_field.send_keys(TEST_EMAIL)
        password_field = WebDriverWait(self.driver, 30).until(lambda d: d.find_element(value='password'))
        password_field.send_keys(TEST_PWD)
        login_button = WebDriverWait(self.driver, 30).until(lambda d: d.find_element(By.XPATH, XPATH_LOGIN_BUTTON))
        login_button.click()
        WebDriverWait(self.driver, 30).until(lambda d: d.find_element(By.XPATH, '//span[text()="Dashboard"]'))
        self.logger.info('Logged in')

    def get_alerts(self):
        self.screenshot()
        alert_elements = WebDriverWait(self.driver, 30).until(lambda d: d.find_elements(By.XPATH, '//*[@role="alert"]'))
        actual_alerts = []
        self.logger.info('-' * 50)
        for alert_element in alert_elements:
            actual_alerts.append(alert_element.text)
            self.logger.info(actual_alerts[-1])
        self.logger.info('-' * 50)
        return tuple(actual_alerts)

    def login_with_validation(self):
        self.logger.info('Login to {}'.format(TEST_BASE_URL))
        self.driver.get(TEST_BASE_URL)
        login_button = WebDriverWait(self.driver, 30).until(lambda d: d.find_element(By.XPATH, XPATH_LOGIN_BUTTON))
        login_button.click()

        self.logger.info('Login form alerts:')
        actual_alerts = self.get_alerts()

        if actual_alerts == LOGIN_ALERTS:
            self.logger.info('Login form alerts succefully validated.')
        else:
            self.logger.error('Unexpected alerts on login page:\n{}\nExpected:\n{}'.format(actual_alerts, LOGIN_ALERTS))

        self.driver.find_element(value='usernameOrEmail').send_keys(TEST_EMAIL)
        self.driver.find_element(value='password').send_keys(TEST_PWD)
        self.driver.find_element(By.XPATH, XPATH_LOGIN_BUTTON).click()
        WebDriverWait(self.driver, 30).until(lambda d: d.find_element(By.XPATH, '//span[text()="Dashboard"]'))
        self.logger.info('Logged in')

    def create_user_form_validation(self):
        self.logger.info('Create user')
        self.driver.get('{}{}'.format(TEST_BASE_URL, POSTFIX_USERS))
        create_user_button = WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element(By.XPATH, '//span[text()="Create User"]'))
        create_user_button.click()

        ext_field = WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element(By.XPATH, '//input[@name="officeNumberExtn"]'))
        ext_field.send_keys('999')
        ext_field.send_keys(3 * Keys.BACKSPACE)
        time.sleep(1)
        save_button = WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element(By.XPATH, '//button[text()="Save"]'))
        save_button.click()

        self.logger.info('Create user alerts:')
        actual_alerts = self.get_alerts()
        if actual_alerts == CREATE_USER_ALERTS_1:
            self.logger.info('Create user form alerts1 succefully validated.')
        else:
            self.logger.error(
                'Unexpected alerts1 on create user:\n{}\nExpected:\n{}'.format(actual_alerts, CREATE_USER_ALERTS_1))

        self.driver.find_element(value='name').send_keys('1')
        self.driver.find_element(value='email').send_keys('2')
        self.driver.find_element(value='password').send_keys('aB1@')
        self.driver.find_element(value='passwordRepeat').send_keys('aB1#')
        combo4 = self.driver.find_elements(By.CLASS_NAME, 'selected-container')[4]
        combo4.click()
        admin_span = WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element(By.XPATH, '//*[text()="Administrator"]'))
        admin_span.click()

        save_button.click()
        self.logger.info('Create user alerts:')
        actual_alerts = self.get_alerts()
        if actual_alerts == CREATE_USER_ALERTS_2:
            self.logger.info('Create user form alerts2 succefully validated.')
        else:
            self.logger.error(
                'Unexpected alerts2 on create user:\n{}\nExpected:\n{}'.format(actual_alerts, CREATE_USER_ALERTS_2))

        self.logger.info('Create user form validation complete')
