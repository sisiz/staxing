import unittest
import sys
import datetime

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait

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
class TestTutorTeacher(unittest.TestCase):
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

    def test_teacher_views_calendar(self):
        ''''''
        today = datetime.date.today()
        today = today.strftime('%B %Y')
        cal_date = self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"calendar-header-label")]' +
                 '/span')
            )
        ).text
        assert(cal_date == today), 'Calendar date is not %s' % today

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_student_scores(self):
        ''''''
        # login teacher
        self.helper.user.login(self.driver,
                               self.helper.user.name,
                               self.helper.user.password,
                               self.helper.user.url)
        # click on student scores
        self.helper.teacher.goto_student_scores(self.driver)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_reference_book(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_roster(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_removes_a_student_from_class(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_moves_a_student_between_periods(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_reading_analytics_aggregate(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_performance_forecast_aggregate(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_performance_forecast(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_external_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_homework_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_reading_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_event_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_review_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_homework(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_homework_details(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_reading(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_reading_details(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_review(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_review_details(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_export_matches_student_scores(self):
        ''''''
