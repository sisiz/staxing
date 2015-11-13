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
    def test_assignment_by_period_draft_to_all_cancel_to_period_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Draft
        # 2nd / 0 / 1 / 1S
        # all / 0 / 1 / 1S / Cancel
        # 1st / 0 / 1 / 1S / Delete
        # 2nd / 0 / 1 / 1S
        name = 'Automated 2'
        description = 'by period draft to all cancel to period delete'
        open_p1 = StaxHelper.date_string()
        close_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        close_p2 = StaxHelper.date_string(2)
        open_all = StaxHelper.date_string()
        close_all = StaxHelper.date_string(1)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, close_p1),
                    '2nd': (open_p2, close_p2), },
                readings=['1.1'],
                status=self.assign.DRAFT, )
        except Exception as ex:
            assert(False), '1: Add :: %s :: %s' % (ex.__class__.__name__, ex)
        try:
            self.assign.change_reading(
                driver=self.driver,
                title=name,
                periods={
                    'all': (open_all, close_all), },
                status=self.assign.CANCEL)
        except Exception as ex:
            assert(False), '2: Edit :: %s :: %s' % (ex.__class__.__name__, ex)
        try:
            self.assign.remove_reading(
                driver=self.driver,
                title=name)
        except Exception as ex:
            assert(False), '3: Remove :: %s :: %s' % \
                (ex.__class__.__name__, ex)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_draft_to_all_draft_to_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Draft
        # 2nd / 1 / 2 / 1S
        # all / 0 / 2 / 1S / Draft
        # all / 0 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_publish_to_all_publish_fail(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Publish
        # 2nd / 0 / 1 / 1S
        # all / 0 / 1 / 1S / Publish **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_publish_to_delete_fail(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Publish
        # 2nd / 1 / 2 / 1S
        # 1st / 0 / 1 / 1S / Delete **
        # 2nd / 1 / 2 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_publish_to_all_publish_to_delete_fail(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Publish
        # 2nd / 1 / 2 / 1S
        # all / 0 / 2 / 1S / Publish
        # all / 0 / 2 / 1S / Delete **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_publish_to_all_cancel_to_period_delete(self):
        '''
        '''
        # 1st / 1 / 2 / 1S / Publish
        # 2nd / 1 / 2 / 1S
        # all / 1 / 2 / 1S / Cancel
        # 1st / 1 / 2 / 1S / Delete
        # 2nd / 1 / 2 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_status_by_period_publish_to_all_publish_to_delete(
            self):
        '''
        '''
        # 1st / 1 / 2 / 1S / Publish
        # 2nd / 1 / 2 / 1S
        # all / 1 / 2 / 1S / Publish
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_publish_to_delete(self):
        '''
        '''
        # 1st / 1 / 2 / 1S / Publish
        # 2nd / 2 / 3 / 1S
        # 1st / 1 / 2 / 1S / Delete
        # 2nd / 2 / 3 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_dates_by_period_publish_to_all_publish_to_delete(self):
        '''
        '''
        # 1st / 1 / 2 / 1S / Publish
        # 2nd / 2 / 3 / 1S
        # all / 1 / 3 / 1S / Publish
        # all / 1 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_cancel(self):
        '''
        '''
        # all / 0 / 1 / 1S / Cancel

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_period_cancel_to_all_delete(self):
        '''
        '''
        # all / 0 / 1 / 1S / Draft
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 0 / 1 / 1S
        # all / 0 / 1 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_period_draft_to_delete(self):
        '''
        '''
        # all / 0 / 1 / 1S / Draft
        # 1st / 0 / 1 / 1S / Draft
        # 2nd / 1 / 2 / 1S
        # 1st / 0 / 1 / 1S / Delete
        # 2nd / 1 / 2 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_all_draft_to_delete(self):
        '''
        '''
        # all / 0 / 1 / 1S / Draft
        # all / 0 / 1 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_all_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1C / Draft
        # all / 1 / 2 / 1C / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_period_publish_to_period_delete_fail(
            self):
        '''
        '''
        # all / 0 / 1 / 1S / Publish
        # 1st / 0 / 1 / 1S / Publish
        # 2nd / 0 / 1 / 1S
        # 1st / 0 / 1 / 1S / Delete **
        # 2nd / 0 / 1 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_period_publish_fail(self):
        '''
        '''
        # all / 0 / 1 / 1S / Publish
        # 1st / 0 / 1 / 1S / Publish **
        # 2nd / 0 / 1 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_delete_fail(self):
        '''
        '''
        # all / 0 / 1 / 1S / Publish
        # all / 0 / 1 / 1S / Delete **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_due_dates_all_draft_to_cancel_to_delete(self):
        '''
        '''
        # all / 0 / 2 / 1S / Draft
        # all / 0 / 1 / 1S / Cancel
        # all / 0 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_open_dates_all_draft_to_cancel_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Draft
        # all / 0 / 2 / 1S / Cancel
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_dates_all_draft_to_cancel_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Draft
        # all / 2 / 3 / 1S / Cancel
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_due_dates_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 0 / 2 / 1S / Draft
        # all / 0 / 1 / 1S / Draft
        # all / 0 / 1 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_due_earlier_all_publish_to_publish_to_delete_fail(
            self):
        '''
        '''
        # all / 0 / 2 / 1S / Publish
        # all / 0 / 1 / 1S / Publish
        # all / 0 / 1 / 1S / Delete **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_due_later_all_publish_to_publish_to_delete_fail(self):
        '''
        '''
        # all / 0 / 2 / 1S / Publish
        # all / 0 / 3 / 1S / Publish
        # all / 0 / 3 / 1S / Delete **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_sections_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1C  / Draft
        # all / 1 / 2 / 1C - 1S / Draft
        # all / 1 / 2 / 1C - 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_draft_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Draft
        # all / 1 / 2 / 1C - 1S / Draft
        # all / 1 / 2 / 1C - 1S / Publish
        # all / 1 / 2 / 1C - 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_plus_sections_all_draft_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Draft
        # all / 1 / 2 / 1C + 1S / Draft
        # all / 1 / 2 / 1C + 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_plus_sections_all_draft_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1S  / Draft
        # all / 1 / 2 / 1S + 1S / Draft
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_plus_sections_all_draft_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Draft
        # all / 1 / 2 / 1C + 1S / Publish
        # all / 1 / 2 / 1C + 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_plus_sections_all_draft_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1S  / Draft
        # all / 1 / 2 / 1S + 1S / Publish
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_minus_sections_all_publish_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Publish
        # all / 1 / 2 / 1C - 1S / Draft
        # all / 1 / 2 / 1C - 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_open_dates_all_publish_to_draft_to_delete(self):
        '''
        '''
        # all / 2 / 3 / 1S / Publish
        # all / 1 / 3 / 1S / Draft
        # all / 1 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_minus_sections_all_publish_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 2S  / Publish
        # all / 1 / 2 / 2S - 1S / Draft
        # all / 1 / 2 / 1S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_ch_minus_sections_all_publish_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Publish
        # all / 1 / 2 / 1C - 1S / Publish
        # all / 1 / 2 / 1C - 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_dates_all_publish_to_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Publish
        # all / 2 / 3 / 1S / Publish
        # all / 2 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_sec_minus_sections_all_publish_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 2S  / Publish
        # all / 1 / 2 / 2S - 1S / Publish
        # all / 1 / 2 / 1S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_plus_sections_all_publish_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Publish
        # all / 1 / 2 / 1C + 1S / Draft
        # all / 1 / 2 / 1C + 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_plus_sections_all_publish_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1S  / Publish
        # all / 1 / 2 / 1S + 1S / Draft
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_plus_sections_all_publish_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Publish
        # all / 1 / 2 / 1C + 1S / Publish
        # all / 1 / 2 / 1C + 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_all_draft_to_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1C / Draft
        # all / 1 / 2 / 1C / Publish
        # all / 1 / 2 / 1C / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_all_publish_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1C / Publish
        # all / 1 / 2 / 1C / Draft
        # all / 1 / 2 / 1C / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_all_publish_to_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1C / Publish
        # all / 1 / 2 / 1C / Publish
        # all / 1 / 2 / 1C / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_plus_sections_all_publish_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1S  / Publish
        # all / 1 / 2 / 1S + 1S / Publish
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_open_dates_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Draft
        # all / 0 / 2 / 1S / Draft
        # all / 0 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_minus_sections_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 2S  / Draft
        # all / 1 / 2 / 2S - 1S / Draft
        # all / 1 / 2 / 1S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_dates_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Draft
        # all / 2 / 3 / 1S / Draft
        # all / 2 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Draft
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_period_cancel_to_all_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Publish
        # 1st / 1 / 2 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_period_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Publish
        # 1st / 1 / 2 / 1S / Publish
        # 2nd / 1 / 2 / 1S
        # 1st / 1 / 2 / 1S / Delete
        # 2nd / 1 / 2 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_publish_to_delete_fail(self):
        '''
        '''
        # all / 1 / 2 / 1S / Publish
        # all / 0 / 2 / 1S / Publish
        # all / 0 / 2 / 1S / Delete **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Publish
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_minus_section_all_draft_to_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 2S  / Draft
        # all / 1 / 2 / 2S - 1S / Publish
        # all / 1 / 2 / 1S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_dates_all_draft_to_publish_to_delete(self):
        '''
        '''
        # all / 2 / 3 / 1S / Draft
        # all / 1 / 3 / 1S / Publish
        # all / 1 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 2S  / Draft
        # all / 1 / 2 / 2S + 1S / Draft
        # all / 1 / 2 / 3S - 1S / Draft
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_publish_to_draft_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 2S  / Draft
        # all / 1 / 2 / 2S + 1S / Publish
        # all / 1 / 2 / 3S - 1S / Draft
        # all / 1 / 2 / 2S  / Publish
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 2S  / Publish
        # all / 1 / 2 / 2S + 1S / Draft
        # all / 1 / 2 / 3S - 1S / Draft
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_publish_to_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 2S  / Publish
        # all / 1 / 2 / 2S + 1S / Publish
        # all / 1 / 2 / 3S - 1S / Publish
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 2 / 3 / 1S / Draft
        # all / 1 / 3 / 1S / Draft
        # all / 1 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_publish_to_delete(self):
        '''
        '''
        # all / 2 / 3 / 1S / Publish
        # all / 1 / 3 / 1S / Publish
        # all / 1 / 3 / 1S / Delete
