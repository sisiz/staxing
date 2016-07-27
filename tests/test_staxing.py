"""Staxing test files."""

import os
import datetime
import pytest
import time
import unittest

from random import randint
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from staxing.assignment import Assignment
from staxing.helper import Helper, Teacher, Student, Admin, ContentQA, User
# from staxing.page_load import SeleniumWait

__version__ = '0.0.3'
TESTS = os.getenv(
    'CASELIST',
    str([
        101, 102, 103, 104, 105, 106,
        201, 202, 203, 204, 205, 206, 207, 208,
        301,
        401,
        501,
        601,
        701,
        801,
    ])
)


class TestStaxingHelper(unittest.TestCase):
    """Staxing case tests for Helper."""

    def setUp(self):
        """Pretest settings."""
        self.helper = Helper()

    def tearDown(self):
        """Test destructor."""
        try:
            self.helper.driver.quit()
        except:
            pass

    @pytest.mark.skipif(str(101) not in TESTS, reason='Excluded')
    def test_helper_set_window_size(self):
        """Set the browser window size."""
        self.helper.set_window_size(1300, 700)
        new_size = {'width': 1300, 'height': 700}
        assert(self.helper.driver.get_window_size() == new_size), \
            'Window not resized: %s' % str(new_size)
        self.helper.driver.set_window_size(200, 200)
        new_size = {'width': 200, 'height': 200}
        self.helper.set_window_size(maximize=True)
        assert(self.helper.driver.get_window_size() != new_size), \
            'Window not maximized: %s' % str(new_size)

    @pytest.mark.skipif(str(102) not in TESTS, reason='Excluded')
    def test_helper_set_new_wait_time(self):
        """Change the wait time."""
        old_wait = self.helper.wait_time
        self.helper.change_wait_time(5)
        new_wait = self.helper.wait_time
        assert(new_wait == 5), 'Wait time not changed: %s' % new_wait
        self.helper.change_wait_time(old_wait)

    @pytest.mark.skipif(str(103) not in TESTS, reason='Excluded')
    def test_helper_date_strings(self):
        """Render multiple date strings."""
        today = datetime.date.today()
        in_5 = today + datetime.timedelta(days=5)
        in_5 = in_5.strftime('%m/%d/%Y')
        formatted = today.strftime('%Y-%m-%d')
        in_12_formatted = today + datetime.timedelta(days=12)
        in_12_formatted = in_12_formatted.strftime('%Y%m%d')
        assert(self.helper.date_string() == today.strftime('%m/%d/%Y')), \
            'Default failed: %s != %s' % (self.helper.date_string(), today)
        assert(self.helper.date_string(5) == str(in_5)), \
            'Set +5 failed: %s != %s' % (self.helper.date_string(5), in_5)
        assert(self.helper.date_string(str_format='%Y-%m-%d') == formatted), \
            'Formatted failed: %s != %s' % (
                self.helper.date_string(str_format='%Y-%m-%d'),
                formatted
            )
        assert(self.helper.date_string(12, '%Y%m%d') == in_12_formatted), \
            'Set +12 formatted failed: %s != %s' % (
                self.helper.date_string(12, '%Y%m%d'),
                in_12_formatted
            )

    @pytest.mark.skipif(str(104) not in TESTS, reason='Excluded')
    def test_helper_get_webpage(self):
        """Get a webpage."""
        self.helper.get('https://www.google.com/')
        assert('Google' in self.helper.driver.title)

    @pytest.mark.skipif(str(105) not in TESTS, reason='Excluded')
    def test_helper_get_window_size(self):
        """Read window size."""
        new_height = randint(300, 600)
        new_width = randint(300, 600)
        self.helper.driver.set_window_size(new_width, new_height)
        current_size = self.helper.driver.get_window_size()
        helper_size = self.helper.get_window_size()
        assert(helper_size == current_size), \
            'Window size is incorrect: %s != %s' % \
            (helper_size, current_size)
        helper_size = self.helper.get_window_size('height')
        assert(helper_size == current_size['height']), \
            'Window height is incorrect: %s != %s' % \
            (helper_size, current_size['height'])
        helper_size = self.helper.get_window_size('width')
        assert(helper_size == current_size['width']), \
            'Window width is incorrect: %s != %s' % \
            (helper_size, current_size['width'])

    @pytest.mark.skipif(str(106) not in TESTS, reason='Excluded')
    def test_helper_sleep_within_two_percent_accuracy(self):
        """Sleep command is accurate to +-2%."""
        sleep_length = randint(3, 8) / 1.0
        start_time = time.time()
        self.helper.sleep(sleep_length)
        end_time = time.time()
        duration = end_time - start_time
        assert(duration >= sleep_length * 0.98), \
            'Sleep shorter than expected: %s < %s' % \
            (duration, sleep_length * 0.98)
        assert(duration <= sleep_length * 1.02), \
            'Sleep longer than expected: %s > %s' % \
            (duration, sleep_length * 1.02)


class TestStaxingUser(unittest.TestCase):
    """Staxing case tests for User."""

    def setUp(self):
        """Pretest settings."""
        self.user = User('', '', '')
        self.server = ''.join(('https://', os.getenv('SERVER_URL')))
        self.login = os.getenv('STUDENT_USER')
        self.password = os.getenv('STUDENT_PASSWORD')

    def tearDown(self):
        """Test destructor."""
        try:
            self.user.driver.quit()
        except:
            pass

    @pytest.mark.skipif(str(201) not in TESTS, reason='Excluded')
    def test_user_tutor_login(self):
        """Log into Tutor."""
        self.user.login(self.server, self.login, self.password)
        was_successful = 'dashboard' in self.user.driver.current_url or \
            'list' in self.user.driver.current_url or \
            'calendar' in self.user.driver.current_url
        assert(was_successful), 'Failed to log into %s' % self.server

    @pytest.mark.skipif(str(202) not in TESTS, reason='Excluded')
    def test_user_tutor_logout(self):
        """Log out of Tutor"""
        self.user.login(self.server, self.login, self.password)
        self.user.logout()
        was_successful = \
            'http://cc.openstax.org/' in self.user.driver.current_url or \
            'https://tutor-qa.openstax.org/?' in self.user.driver.current_url
        assert(was_successful), 'Failed to log out of %s' % self.server

    @pytest.mark.skipif(str(203) not in TESTS, reason='Excluded')
    def test_user_accounts_login(self):
        """Log into Accounts."""
        accounts = self.server.replace('tutor', 'accounts')
        self.user.login(accounts, self.login, self.password)
        assert('profile' in self.user.driver.current_url), \
            'Failed to log into %s' % accounts

    @pytest.mark.skipif(str(204) not in TESTS, reason='Excluded')
    def test_user_accounts_logout(self):
        """Log out of Accounts."""
        accounts = self.server.replace('tutor', 'accounts')
        self.user.login(accounts, self.login, self.password)
        self.user.logout()
        assert('signin' in self.user.driver.current_url), \
            'Failed to log out of %s' % accounts

    @pytest.mark.skipif(str(205) not in TESTS, reason='Excluded')
    def test_user_select_course_by_title(self):
        """Select a course by its title."""
        self.user.login(self.server, self.login, self.password)
        courses = self.user.driver.find_elements(
            By.CLASS_NAME,
            'tutor-course-item'
        )
        course_number = randint(0, len(courses) - 1)
        title = courses[course_number].text
        Assignment.scroll_to(self.user.driver, courses[course_number])
        self.user.select_course(title=title)
        was_successful = 'courses' in self.user.driver.current_url or \
            'list' in self.user.driver.current_url or \
            'calendar' in self.user.driver.current_url or \
            'contents' in self.user.driver.current_url
        assert(was_successful), \
            'Failed to select course in URL: %s' % self.user.driver.current_url
        if 'contents' in self.user.driver.current_url:
            return
        course_name = self.user.driver.find_element(
            By.CLASS_NAME,
            'course-name'
        ).text
        assert(title == course_name), 'Failed to select course "%s"' % title

    @pytest.mark.skipif(str(206) not in TESTS, reason='Excluded')
    def test_user_select_course_by_appearance(self):
        """Select a course by its appearance."""
        self.user.login(self.server, self.login, self.password)
        courses = self.user.driver.find_elements(
            By.CLASS_NAME,
            'tutor-booksplash-course-item'
        )
        course_number = randint(0, len(courses) - 1)
        appearance = courses[course_number].get_attribute('data-appearance')
        appearance_courses = self.user.driver.find_elements(
                By.XPATH,
                '//div[contains(@data-appearance,"%s")]' % appearance
            )
        title = ''
        if isinstance(appearance_courses, list):
            for course in appearance_courses:
                title = title.join((' ', course.text))
        else:
            title = courses[course_number].text
        Assignment.scroll_to(self.user.driver, courses[course_number])
        self.user.select_course(appearance=appearance)
        was_successful = 'courses' in self.user.driver.current_url or \
            'list' in self.user.driver.current_url or \
            'calendar' in self.user.driver.current_url or \
            'contents' in self.user.driver.current_url
        assert(was_successful), \
            'Failed to select course in URL: %s' % self.user.driver.current_url
        if 'contents' in self.user.driver.current_url:
            return
        course_name = self.user.driver.find_element(
            By.CLASS_NAME,
            'course-name'
        ).text
        assert(course_name in title), \
            'Failed to select course "%s"' % course_name

    @pytest.mark.skipif(str(207) not in TESTS, reason='Excluded')
    def test_user_go_to_course_list(self):
        """No test placeholder."""
        self.user.login(self.server, self.login, self.password)
        courses = self.user.driver.find_elements(
            By.CLASS_NAME,
            'tutor-course-item'
        )
        course_number = randint(0, len(courses) - 1)
        Assignment.scroll_to(self.user.driver, courses[course_number])
        self.user.select_course(title=courses[course_number].text)
        was_successful = 'courses' in self.user.driver.current_url or \
            'list' in self.user.driver.current_url or \
            'calendar' in self.user.driver.current_url
        assert(was_successful), 'Failed to select course'
        self.user.goto_course_list()
        course_picker = self.server + '/dashboard/'
        assert(self.user.driver.current_url == course_picker), \
            'Failed to return to the course picker'

    @pytest.mark.skipif(str(208) not in TESTS, reason='Excluded')
    def test_user_open_the_reference_book(self):
        """No test placeholder."""
        self.user.login(self.server, self.login, self.password)
        main_window = self.user.driver.current_window_handle
        courses = self.user.driver.find_elements(
            By.CLASS_NAME,
            'tutor-course-item'
        )
        course_number = randint(0, len(courses) - 1)
        Assignment.scroll_to(self.user.driver, courses[course_number])
        self.user.select_course(title=courses[course_number].text)
        was_successful = 'courses' in self.user.driver.current_url or \
            'list' in self.user.driver.current_url or \
            'calendar' in self.user.driver.current_url
        assert(was_successful), 'Failed to select course'
        self.user.view_reference_book()
        self.user.driver.switch_to_window(self.user.driver.window_handles[1])
        WebDriverWait(self.user.driver, 60).until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'center-panel')
            )
        )
        assert('contents' in self.user.driver.current_url or
               'books' in self.user.driver.current_url), \
            'Failed to open the reference or WebView book.'
        self.user.driver.close()
        self.user.driver.switch_to_window(main_window)
        was_successful = 'courses' in self.user.driver.current_url or \
            'list' in self.user.driver.current_url or \
            'calendar' in self.user.driver.current_url
        assert(was_successful), 'Failed to return to the primary browser tab'


class TestStaxingTutorTeacher(unittest.TestCase):
    """Staxing case tests."""

    def setUp(self):
        """Pretest settings."""
        self.teacher = Teacher(use_env_vars=True)

    def tearDown(self):
        """Test destructor."""
        try:
            self.teacher.driver.quit()
        except:
            pass

    @pytest.mark.skipif(str(301) not in TESTS, reason='Excluded')
    def test_base_case(self):
        """No test placeholder."""
        pass


class TestStaxingConceptCoachTeacher(unittest.TestCase):
    """Staxing case tests."""

    def setUp(self):
        """Pretest settings."""
        self.teacher = Teacher(username='', password='', site='')

    def tearDown(self):
        """Test destructor."""
        try:
            self.teacher.driver.quit()
        except:
            pass

    @pytest.mark.skipif(str(401) not in TESTS, reason='Excluded')
    def test_base_case(self):
        """No test placeholder."""
        pass


class TestStaxingTutorStudent(unittest.TestCase):
    """Staxing case tests."""

    def setUp(self):
        """Pretest settings."""
        self.student = Student(use_env_vars=True)

    def tearDown(self):
        """Test destructor."""
        try:
            self.student.driver.quit()
        except:
            pass

    @pytest.mark.skipif(str(501) not in TESTS, reason='Excluded')
    def test_base_case(self):
        """No test placeholder."""
        pass


class TestStaxingConceptCoachStudent(unittest.TestCase):
    """Staxing case tests."""

    def setUp(self):
        """Pretest settings."""
        self.student = Student(use_env_vars=True)

    def tearDown(self):
        """Test destructor."""
        try:
            self.student.driver.quit()
        except:
            pass

    @pytest.mark.skipif(str(601) not in TESTS, reason='Excluded')
    def test_base_case(self):
        """No test placeholder."""
        pass


class TestStaxingAdmin(unittest.TestCase):
    """Staxing case tests."""

    def setUp(self):
        """Pretest settings."""
        self.admin = Admin(use_env_vars=True)

    def tearDown(self):
        """Test destructor."""
        try:
            self.admin.driver.quit()
        except:
            pass

    @pytest.mark.skipif(str(701) not in TESTS, reason='Excluded')
    def test_base_case(self):
        """No test placeholder."""
        pass


class TestStaxingContentQA(unittest.TestCase):
    """Staxing case tests."""

    def setUp(self):
        """Pretest settings."""
        self.content = ContentQA(use_env_vars=True)

    def tearDown(self):
        """Test destructor."""
        try:
            self.content.driver.quit()
        except:
            pass

    @pytest.mark.skipif(str(801) not in TESTS, reason='Excluded')
    def test_base_case(self):
        """No test placeholder."""
        pass
