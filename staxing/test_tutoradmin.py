import unittest
import sys
import datetime

# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
# import datetime

from pastasauce import PastaSauce, PastaDecorator
from . import StaxHelper

NOT_STARTED = True
if NOT_STARTED:
    import pytest

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


@PastaDecorator.on_platforms(browsers)
class TestTutorAdmin(unittest.TestCase):
    ''''''
    def setUp(self):
        self.ps = PastaSauce()
        self.helper = StaxHelper()
        self.desired_capabilities['name'] = self.id()
        student = self.helper.student.name
        student_password = self.helper.student.password
        self.driver = StaxHelper.run_on(
            StaxHelper.LOCAL, self.ps, self.desired_capabilities
        )
        self.driver.implicitly_wait(15)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.set_window_size(*standard_window)
        self.helper.user.login(self.driver, student, student_password,
                               self.helper.user.url)
        self.helper.user.select_course(self.driver, category='Physics')
        self.screenshot_path = '~/Desktop/ScreenshotErrors'

        # # # TODO: setup test assignments # # #

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

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_add_period_to_a_course(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_changes_period_name(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_adds_student_to_period(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_removes_student_from_course(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_moves_student_to_another_period(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_imports_a_new_ecosystem_book(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_edits_a_course(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_impersonates_a_teacher(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_impersonates_a_student(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_creates_a_new_user_account(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_adds_a_teacher_to_a_course(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_creates_a_district(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_edits_a_district(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_deletes_a_district(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_creates_a_school(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_edits_a_school(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_deletes_a_school(self):
        ''''''
