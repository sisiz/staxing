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
class TestTutorStudent(unittest.TestCase):
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
    def test_student_views_dashboard(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_views_all_past_work(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_views_reference_book(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_works_a_standard_reading(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_works_an_intro_reading(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_works_a_homework(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_practices_weakest_topics_from_dashboard(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_practices_specific_topic_from_dashboard(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_views_complete_performance_forecast(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_practices_all_topics_from_forecast(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_practices_one_chapter_from_forecast(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_practices_specific_topic_from_forecast(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_works_an_external_assignment(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_reviews_a_finished_reading(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_student_reviews_a_finished_homework(self):
        ''''''
