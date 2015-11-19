import unittest
import pytest

# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

from pastasauce import PastaSauce, PastaDecorator
from . import StaxHelper

NOT_STARTED = True

browsers = [{
    "platform": "Windows 7",
    "browserName": "firefox",
    "version": "40.0",
    "screenResolution": "1440x900"
}]

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
        self.rword = self.helper.user.assignment.rword
        self.screenshot_path = '/tmp/errors/'

    def tearDown(self):
        # Returns the info of exception being handled
        has_errors = self._test_has_failed()
        if has_errors:
            print(self.driver.current_url, '\n')
            date_and_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
            filename = 'testerr_%s.png' % date_and_time
            self.driver.save_screenshot('%s%s' % (self.screenshot_path,
                                        filename))
        self.driver.quit()
        self.ps.update_job(self.driver.session_id, passed=has_errors)

    def _test_has_failed(self):
        # for 3.4. In 3.3, can just use self._outcomeForDoCleanups.success:
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

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
