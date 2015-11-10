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
class TestTutorAssignments(unittest.TestCase):
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
    def test_assignment_all_plus_cancel(self):
        '''
        all  0    1    1S  cancel
        all  0    2,1  1S  cancel
        all  0    2,3  1S  cancel
        all  1    2    1S  cancel
        all  1,2  2,3  1S  cancel
        all  1,0  2    1S  cancel
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_plus_cancel(self):
        '''
        by_period  0  1  1S  cancel
        by_period  1  2  1S  cancel
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_plus_draft(self):
        '''
        all  0    1    1S  draft
        all  0    2,1  1S  draft
        all  0    2,3  1S  draft
        all  1    2    1S  draft
        all  1,2  2,3  1S  draft
        all  1,0  2    1S  draft
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_plus_draft(self):
        '''
        by_period  0  1  1S  draft
        by_period  1  2  1S  draft
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_mix_plus_draft_and_cancel(self):
        '''
        all + by_period  0  1  1S  draft + cancel
        by_period + all  0  1  1S  draft + cancel
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_plus_draft_and_delete(self):
        '''
        all  0    1    1S  draft + delete
        all  0    2,1  1S  draft + delete
        all  0    2,3  1S  draft + delete
        all  1    2    1S  draft + delete
        all  1,2  2,3  1S  draft + delete
        all  1,0  2    1S  draft + delete
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_and_by_period_plus_draft_and_delete(self):
        '''
        all + by_period  0  1  1S  draft + delete
        all + by_period  1  2  1S  draft + delete
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_plus_draft_and_delete(self):
        '''
        by_period  0  1  1S  draft + delete
        by_period  1  2  1S  draft + delete
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_and_all_plus_draft_and_delete(self):
        '''
        by_period + all  0  1  1S  draft + delete
        by_period + all  1  2  1S  draft + delete
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_plus_draft_and_draft(self):
        '''
        all  1    2  1C               draft + draft
        all  1    2  1C - 1S          draft + draft
        all  1    2  1C + 1S          draft + draft
        all  1    2  1S + 1S          draft + draft
        all  1    2  2S - 1S          draft + draft
        all  1    2  2S + (+1S, -1S)  draft + draft
        all  2,1  3  1S               draft + draft
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_and_by_period_plus_draft_and_draft(self):
        '''
        all + by_period  0  1  1S  draft + draft
        all + by_period  1  2  1S  draft + draft
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_and_all_plus_draft_and_draft(self):
        '''
        by_period + all  0  1  1S  draft + draft
        by_period + all  1  2  1S  draft + draft
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_plus_draft_and_publish(self):
        '''
        all  1    2  1C               draft + publish
        all  1    2  1C - 1S          draft + publish
        all  1    2  1C + 1S          draft + publish
        all  1    2  1S + 1S          draft + publish
        all  1    2  2S - 1S          draft + publish
        all  1    2  2S + (+1S, -1S)  draft + publish
        all  2,1  3  1S               draft + publish
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_plus_publish(self):
        '''
        all  0    1    1S  publish
        all  0    2,1  1S  publish
        all  0    2,3  1S  publish
        all  1    2    1S  publish
        all  1,2  2,3  1S  publish
        all  1,0  2    1S  publish
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_plus_publish(self):
        '''
        by_period  0  1  1S  publish
        by_period  1  2  1S  publish
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_mix_plus_publish_and_cancel(self):
        '''
        all + by_period  1  2  1S  publish + cancel
        by_period + all  1  2  1S  publish + cancel
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_plus_publish_and_delete(self):
        '''
        all  0    1    1S  publish + delete
        all  0    2,1  1S  publish + delete
        all  0    2,3  1S  publish + delete
        all  1    2    1S  publish + delete
        all  1,2  2,3  1S  publish + delete
        all  1,0  2    1S  publish + delete
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_and_by_period_plus_publish_and_delete(self):
        '''
        all + by_period  0  1  1S  publish + delete
        all + by_period  1  2  1S  publish + delete
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_plus_publish_and_delete(self):
        '''
        by_period  0  1  1S  publish + delete
        by_period  1  2  1S  publish + delete
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_and_all_plus_publish_and_delete(self):
        '''
        by_period + all  0  1  1S  publish + delete
        by_period + all  1  2  1S  publish + delete
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_plus_publish_and_draft(self):
        '''
        all  1    2  1C               publish + draft
        all  1    2  1C - 1S          publish + draft
        all  1    2  1C + 1S          publish + draft
        all  1    2  1S + 1S          publish + draft
        all  1    2  2S - 1S          publish + draft
        all  1    2  2S + (+1S, -1S)  publish + draft
        all  2,1  3  1S               publish + draft
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_plus_publish_and_publish(self):
        '''
        all  1    2  1C               publish + publish
        all  1    2  1C - 1S          publish + publish
        all  1    2  1C + 1S          publish + publish
        all  1    2  1S + 1S          publish + publish
        all  1    2  2S - 1S          publish + publish
        all  1    2  2S + (+1S, -1S)  publish + publish
        all  2,1  3  1S               publish + publish
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_and_by_period_plus_publish_and_publish(self):
        '''
        all + by_period  0  1  1S  publish + publish
        all + by_period  1  2  1S  publish + publish
        '''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_and_all_plus_publish_and_publish(self):
        '''
        by_period + all  0  1  1S  publish + publish
        by_period + all  1  2  1S  publish + publish
        '''
