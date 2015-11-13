import unittest
import sys
import datetime
import pytest
import inspect

# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
# import datetime

from pastasauce import PastaSauce, PastaDecorator
from . import StaxHelper

browsers = [{
    "platform": "Windows 10",
    "browserName": "internet explorer",
    "version": "11"
}, {
    "platform": "OS X 10.11",
    "browserName": "safari",
    "version": "8.1"
}, {
    "platform": "Windows 7",
    "browserName": "internet explorer",
    "version": "11.0",
    "screenResolution": "1440x900"
}, {
    "platform": "Windows 7",
    "browserName": "chrome",
    "version": "44.0",
    "screenResolution": "1440x900"
}, {
    "platform": "Windows 7",
    "browserName": "firefox",
    "version": "40.0",
    "screenResolution": "1440x900"
}, {
    "platform": "OS X 10.9",
    "browserName": "iPhone",
    "version": "7.1",
    "deviceName": "iPad Retina (64-bit)",
    "deviceOrientation": "portrait"
}]
# use 1 browser setup
browsers = [browsers[4]]
standard_window = (1440, 800)
compressed_window = (700, 500)

NOT_STARTED = True


@PastaDecorator.on_platforms(browsers)
class TestTutorBasicAssignments(unittest.TestCase):
    ''''''
    def setUp(self):
        self.ps = PastaSauce()
        self.helper = StaxHelper()
        self.desired_capabilities['name'] = self.id()
        teacher = self.helper.user.name
        teacher_password = self.helper.user.password
        self.driver = StaxHelper.run_on(
            StaxHelper.LOCAL, self.ps, self.desired_capabilities
        )
        self.driver.implicitly_wait(15)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.set_window_size(*standard_window)
        self.helper.user.login(self.driver, teacher, teacher_password,
                               self.helper.user.url)
        self.helper.user.select_course(self.driver, category='Physics')
        self.screenshot_path = '~/Desktop/ScreenshotErrors'
        self.assign = self.helper.user.assignment
        self.today = StaxHelper.date_string(today=True)

    def tearDown(self):
        if sys.exc_info()[0]:  # Returns the info of exception being handled
            fail_url = self.driver.current_url
            print(fail_url)
            now = 'testerr_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
            self.driver.get_screenshot_as_file(
                self.screenshot_path +
                '' if self.screenshot_path[-1:] == '/' else '/' +
                '%s.png' % now)
        self.driver.quit()
        status = (sys.exc_info() == (None, None, None))
        self.ps.update_job(self.driver.session_id, passed=status)

    # @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_all_cancel(self):
        '''
        '''
        # all / 0 / 1 / 1S / Cancel
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 1'
        description = 'by period cancel'
        open_all = StaxHelper.date_string()
        due_all = StaxHelper.date_string(1)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    'all': (open_all, due_all), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_all_draft_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 2'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_all_publish(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 3'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_by_period_cancel(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 4'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_by_period_draft_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 5'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_by_period_publish(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 6'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_all_cancel(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 7'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_all_draft_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 8'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_all_publish_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 9'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_by_period_cancel(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 10'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_by_period_draft_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 11'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_by_period_publish_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 12'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)
