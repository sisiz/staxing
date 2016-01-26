# a helper to use actions

import datetime
import inspect
import os
import sys
import time
import unittest

from builtins import FileNotFoundError
from requests import HTTPError
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from urllib.parse import urlparse, ParseResult

if __name__ == '__main__':
    from assignment import Assignment
else:
    try:
        from staxing.assignment import Assignment
    except ImportError:
        from assignment import Assignment


class StaxHelper(object):
    ''''''
    CONDENSED_WIDTH = 767  # pixels
    DEFAULT_WAIT_TIME = 15  # seconds

    def __init__(self, driver_type='chrome', capabilities=None,
                 pasta_user=None, wait_time=DEFAULT_WAIT_TIME,
                 opera_driver='/Applications/operadriver'):
        self.webdriver_service = None
        if driver_type == 'saucelabs' and pasta_user is None:
            raise TypeError('A Sauce Labs user is required for remote testing')
        try:
            self.driver = {
                'firefox': lambda: webdriver.Firefox(),
                'chrome': lambda: webdriver.Chrome(),
                'ie': lambda: webdriver.Ie(),
                'opera': lambda: self.start_opera(opera_driver),
                'phantomjs': lambda: webdriver.PhantomJS(),
                'saucelabs': lambda: webdriver.Remote(
                    command_executor=(
                        'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' %
                        (pasta_user.get_user(), pasta_user.get_access_key())
                    ),
                    desired_capabilities=capabilities
                ),
            }[driver_type]()
        except WebDriverException as err:
            raise FileNotFoundError(err)
        except Exception as err:
            raise self.WebDriverTypeException(
                msg='Unknown WebDriver type: "%s"' % driver_type,
                err=err.__traceback__
            )
        self.wait = WebDriverWait(self.driver, wait_time)

    def start_opera(self, location):
        from selenium.webdriver.chrome import service
        self.webdriver_service = service.Service(location)
        self.webdriver_service.start()
        self.driver = webdriver.Remote(
            self.webdriver_service.service_url,
            webdriver.DesiredCapabilities.OPERA
        )

    @classmethod
    def date_string(cls, day_delta=0, str_format='%m/%d/%Y'):
        return (datetime.date.today() + datetime.timedelta(days=day_delta)). \
            strftime(str_format)

    def quit(self):
        self.webdriver_service.stop() if \
            self.webdriver_service is not None else self.driver.quit()
        sleep(1)
        del self

    def get(self, url):
        self.driver.get(url)

    def get_window_size(self, dimension=None):
        get_size = self.driver.get_window_size()
        if dimension is None:
            return get_size
        if dimension not in get_size:
            raise IndexError('Unknown dimension: %s' % dimension)
        return get_size[dimension]

    class WebDriverTypeException(WebDriverException):
        def __init__(self, msg, err):
            self.msg = msg
            self.__traceback__ = err

        def __str__(self):
            return repr(self.msg, self.__traceback__)


class User(object):
    ''''''
    def __init__(self, helper=None, user='None', username=None, password=None,
                 site=None, email=None):
        self.sh = helper
        self.user_type = user
        self.username = username
        self.password = password
        parse = urlparse(site)
        if parse.scheme != 'https':
            parse = list(parse)
            parse[0] = 'https'
            parse = ParseResult(*parse)
            self.url = parse.geturl()
        else:
            self.url = site
        self.email = email

    def login(self, username=None, password=None, url=None):
        '''
        Tutor login control

        Requires a Tutor or Accounts instance
        Branching to deal with standard or compact screen widths
        '''
        driver = self.sh.driver
        wait = self.sh.wait
        url_address = self.url if url is None else url
        # open the URL
        driver.get(url_address)
        if 'tutor' in url_address:
            # check to see if the screen width is normal or condensed
            if self.sh.get_window_size('width') <= \
                    StaxHelper.CONDENSED_WIDTH:
                # get small-window menu toggle
                is_collapsed = driver.find_element(
                    By.XPATH,
                    '//button[contains(@class,"navbar-toggle")]'
                )
                # check if the menu is collapsed and, if yes, open it
                if('collapsed' in is_collapsed.get_attribute('class')):
                    is_collapsed.click()
            driver.find_element(By.LINK_TEXT, 'Login').click()
        wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//html/body')
            )
        )
        import re
        src = driver.page_source
        text_located = re.search(r'openstax', src.lower()) is not None
        if not text_located:
            raise self.LoginError('Non-OpenStax URL: %s' %
                                  driver.current_url)
        # enter the username and password
        driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.username if username is None else username)
        driver.find_element(By.ID, 'password'). \
            send_keys(self.password if password is None else password)
        # click on the sign in button
        driver.find_element(
            By.XPATH, '//button[text()="Sign in"]'
        ).click()

    def logout(self):
        '''
        Logout control
        '''
        url_address = self.sh.driver.current_url
        if 'tutor' in url_address:
            self.tutor_logout()
        elif 'accounts' in url_address:
            self.accounts_logout()
        else:
            raise HTTPError('Not an OpenStax URL')

    def open_user_menu(self):
        '''
        Hamburger menu opener

        ToDo: branching to handle if a toggle is already open
        '''
        if self.sh.get_window_size('width') <= StaxHelper.CONDENSED_WIDTH:
            # compressed window display on Tutor
            self.sh.wait.until(
                expect.visibility_of_element_located(
                    (By.CLASS_NAME, 'navbar-toggle')
                )
            ).click()
        self.sh.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'dropdown-toggle')
            )
        ).click()

    def tutor_logout(self):
        '''
        Tutor logout helper
        '''
        self.open_user_menu()
        self.sh.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[@aria-label="Sign out"]')
            )
        ).click()

    def accounts_logout(self):
        '''
        Accounts logout helper
        '''
        self.sh.driver.find_element(By.LINK_TEXT, 'Sign out').click()

    def select_course(self, title=None, category=None):
        '''
        Course selection

        ToDo: allow selection of course 3 or higher
        '''
        if 'dashboard' not in self.sh.driver.current_url:
            return
        if title:
            uses_option = 'title'
            course = title
        elif category:
            uses_option = 'category'
            course = category.lower()
        else:
            raise self.LoginError('Unknown course selection "%s"' %
                                  title if title else category)
        self.sh.wait.until(
            expect.element_to_be_clickable(
                (
                    By.XPATH, '//div[@data-%s="%s"]//a' %
                    (uses_option, course)
                )
            )
        ).click()

    def view_reference_book(self):
        '''
        Access the reference book
        '''
        driver = self.sh.driver
        browse = driver.find_element(
            By.XPATH, '//div/a[contains(@class,"view-reference-guide")]')
        if browse:
            browse.click()
            return
        self.open_user_menu()
        driver.find_element(
            By.XPATH, '//li/a[contains(@class,"view-reference-guide")]'
        ).click()

    class LoginError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)


class Teacher(User):
    ''''''
    def __init__(self, helper=None, user='teacher', username=None,
                 password=None, site=None, email=None, use_env_vars=False):
        if use_env_vars:
            username = os.environ['TEACHER_USER']
            password = os.environ['TEACHER_PASSWORD']
        super().__init__(helper, user, username, password, site, email)

    def add_assignment(self, assignment, args):
        '''
        Add an assignment
        '''
        assign = Assignment()
        assign.add[assignment](
            driver=self.sh.driver,
            name=args['title'],
            description=args['description'],
            periods=args['periods'],
            state=args['status'],
            url=args['url'] if 'url' in args else None,
            reading_list=args['reading_list'] if 'reading_list' in args else
            None,
            problems=args['problems'] if 'problems' in args else None,
        )

    def change_assignment(self, assignment, args):
        '''
        Alter an existing assignment
        '''
        assign = Assignment()
        assign.edit[assignment](
            driver=self.sh.driver,
            name=args['title'],
            description=args['description'],
            periods=args['periods'],
            state=args['status'],
            url=args['url'] if 'url' in args else None,
            reading_list=args['reading_list'] if 'reading_list' in args else
            None,
            problems=args['problems'] if 'problems' in args else None,
        )

    def delete_assignment(self, assignment, args):
        '''
        Delete an existing assignment (if available)
        '''
        assign = Assignment()
        assign.remove[assignment](
            driver=self.sh.driver,
            name=args['title'],
            description=args['description'],
            periods=args['periods'],
            state=args['status'],
            url=args['url'] if 'url' in args else None,
            reading_list=args['reading_list'] if 'reading_list' in args else
            None,
            problems=args['problems'] if 'problems' in args else None,
        )

    def goto_menu_item(self, item):
        '''
        Go to a specific user menu item
        '''
        driver = self.sh.driver
        if 'courses' in driver.current_url:
            User.open_user_menu(driver)
            self.sh.wait.until(
                expect.element_to_be_clickable(
                    (By.LINK_TEXT, item)
                )
            ).click()

    def goto_calendar(self):
        '''
        Return the teacher to the calendar dashboard
        '''
        try:
            self.sh.driver.find_element(
                By.XPATH, '//a[contains(@class,"navbar-brand")]'
            ).click()
            return
        except:
            pass
        self.goto_menu_item('Dashboard')

    def goto_performance_forecast(self):
        '''
        Access the performance forecast page
        '''
        self.goto_menu_item('Performance Forecast')

    def goto_student_scores(self):
        '''
        Access the student scores page
        '''
        self.goto_menu_item('Student Scores')


class Student(User):
    ''''''
    def __init__(self, helper=None, user='student', username=None,
                 password=None, site=None, email=None, use_env_vars=False):
        if use_env_vars:
            username = os.environ['STUDENT_USER']
            password = os.environ['STUDENT_PASSWORD']
        super().__init__(helper, user, username, password, site, email)

    def work_assignment(self):
        '''
        Work an assignment

        ToDo: all
        '''
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    def goto_past_work(self):
        '''
        View work for previous weeks

        ToDo: all
        '''
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    def goto_performance_forecast(self):
        '''
        View the student performance forecast

        ToDo: all
        '''
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    def practice(self):
        '''
        Complete a set of 5 practice problems

        ToDo: all
        '''
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


class Admin(User):
    ''''''
    def __init__(self, helper=None, user='admin', username=None, password=None,
                 site=None, email=None, use_env_vars=False):
        if use_env_vars:
            username = os.environ['ADMIN_USER']
            password = os.environ['ADMIN_PASSWORD']
        super().__init__(helper, user, username, password, site, email)

    def goto_admin_control(self):
        '''
        Access the administrator controls
        '''
        wait = self.sh.wait
        wait.until(
            expect.visibility_of_element_located(
                (
                    By.XPATH,
                    '//li[contains(@class,"-hamburger-menu")]/' +
                    'a[@type="button"]'
                )
            )
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Admin')
            )
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Admin Console"]')
            )
        )

    def goto_courses(self):
        '''
        Access the course admin control
        '''
        wait = self.sh.wait
        try:
            wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Admin Console"]')
                )
            )
        except:
            self.goto_admin_control()
        organization = wait.until(
            expect.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        )
        if 'open' not in organization.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            organization.click()
        wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Courses')
            )
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Courses"]')
            )
        )

    def goto_ecosystems(self):
        '''
        Access the ecosystem admin control
        '''
        wait = self.sh.wait
        try:
            wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Admin Console"]')
                )
            )
        except:
            self.goto_admin_control()
        content = wait.until(
            expect.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        )
        if 'open' not in content.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            content.click()
        wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Ecosystems')
            )
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Ecosystems"]')
            )
        )


class ContentQA(User):
    ''''''
    def __init__(self, helper=None, user='content', username=None,
                 password=None, site=None, email=None, use_env_vars=False):
        if use_env_vars:
            username = os.environ['CONTENT_USER']
            password = os.environ['CONTENT_PASSWORD']
        super().__init__(helper, user, username, password, site, email)


class TestStaxHelper(unittest.TestCase):
    def test_staxhelper_chrome(self):
        try:
            helper = StaxHelper().quit()
            helper = StaxHelper()
            user = User(helper)
            del user
            helper.quit()
            helper = StaxHelper(driver_type='chrome').quit()
        except FileNotFoundError or WebDriverException:
            print('\n> Chrome Driver not available <')
        finally:
            if bool(helper.driver):
                helper.driver.quit()

    def test_staxhelper_firefox(self):
        try:
            StaxHelper(driver_type='firefox').quit()
        except FileNotFoundError or WebDriverException:
            print('\n> FireFox Driver not available <')

    @unittest.skipIf(sys.platform == 'darwin', 'No IE on Mac')
    def test_staxhelper_ie(self):
        try:
            StaxHelper(driver_type='ie').quit()
        except FileNotFoundError or WebDriverException:
            print('\n> Internet Explorer Driver not available <')

    def test_staxhelper_opera(self):
        try:
            StaxHelper(driver_type='opera').quit()
        except FileNotFoundError or WebDriverException:
            print('\n> Opera Driver not available <')

    @unittest.skipIf(True, 'PhantomJS is not implemented')
    def test_staxhelper_phantomjs(self):
        try:
            StaxHelper(driver_type='phantomjs').quit()
        except FileNotFoundError or WebDriverException:
            print('\n> PhantomJS Driver not available <')

    def test_staxhelper_init_errs(self):
        with self.assertRaises(TypeError):
            StaxHelper(driver_type='saucelabs')
        with self.assertRaises(StaxHelper.WebDriverTypeException):
            StaxHelper(driver_type='no driver type')


class TestUser(unittest.TestCase):
    def setUp(self):
        self.helper = StaxHelper()
        self.user = User(helper=self.helper)

    def tearDown(self):
        self.helper.quit()

    def test_user_object(self):
        assert(self.user.username is None), 'Username is set'
        assert(self.user.password is None), 'Password is set'
        assert(self.user.url is not None), 'URL is not parsed or is invalid'
        assert(self.user.email is None), 'E-mail is set'

    def test_user_login(self):
        self.user.login('student01', 'password',
                        'https://tutor-qa.openstax.org/')


class TestTeacherUser(unittest.TestCase):
    def setUp(self):
        self.user = Teacher()

    def tearDown(self):
        ''''''


class TestStudentUser(unittest.TestCase):
    def setUp(self):
        self.user = Student()

    def tearDown(self):
        ''''''


class TestAdminUser(unittest.TestCase):
    def setUp(self):
        self.user = Admin()

    def tearDown(self):
        ''''''


class TestContentQAUser(unittest.TestCase):
    def setUp(self):
        self.user = ContentQA()

    def teardown(self):
        ''''''


class TestAssignments(unittest.TestCase):
    def setUp(self):
        self.today = datetime.date.today()
        self.helper = StaxHelper()
        self.user = Teacher(helper=self.helper,
                            site='http://tutor-qa.openstax.org/',
                            username='physics',
                            password='password')

    def tearDown(self):
        self.user.helper = None
        try:
            self.helper.quit()
        except:
            pass

    def test_assignments(self):
        begin = (self.today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (self.today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # start the code example
        self.user.login()
        self.user.select_course(category='physics')
        for chap in ['ch11', 'ch12']:
            reading = 'v6.131 chapter %s' % chap
            self.user.add_assignment(
                assignment='reading',
                args={
                    'title': reading,
                    'description': 'A diagnostic assignment for %s' % chap,
                    'periods': {'all': (begin, end)},
                    'reading_list': [chap],
                    'status': 'publish',
                }
            )
            time.sleep(5)
        homework = 'test-hw %s' % Assignment.rword(8)
        self.user.add_assignment(
            assignment='homework',
            args={
                'title': homework,
                'description': 'An auto-test assignment',
                'periods': {'all': (begin, end)},
                'problems': {'4': None,
                             '4.1': (4, 8),
                             '4.2': 'all',
                             '4.3': ['2102@1', '2104@1', '2175'],
                             'ch5': 5,
                             'tutor': 4},
                'status': 'draft',
            }
        )


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()
