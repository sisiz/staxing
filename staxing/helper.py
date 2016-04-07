"""OpenStax Python helper for common actions."""

import datetime
import inspect
import os
import re

from builtins import FileNotFoundError
from requests import HTTPError
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from urllib.parse import urlparse, ParseResult

try:
    from staxing.assignment import Assignment
except ImportError:
    from assignment import Assignment
try:
    from staxing.page_load import SeleniumWait as Page
except ImportError:
    from page_load import SeleniumWait as Page
__version__ = '0.1.0'


class Helper(object):
    """Primary parent control class."""

    CONDENSED_WIDTH = 767  # pixels wide
    DEFAULT_WAIT_TIME = 15  # seconds

    def __init__(self, driver_type='chrome', capabilities=None,
                 pasta_user=None, wait_time=DEFAULT_WAIT_TIME,
                 opera_driver=''):
        """Class constructor."""
        if driver_type == 'saucelabs' and pasta_user is None:
            raise TypeError('A Sauce Labs user is required for remote testing')
        self.pasta = pasta_user
        self.opera_driver = opera_driver
        self.driver = self.run_on(driver_type=driver_type,
                                  pasta_user=self.pasta,
                                  capabilities=capabilities)
        self.driver.implicitly_wait(wait_time)
        self.wait = WebDriverWait(self.driver, wait_time)
        self.wait_time = wait_time
        self.page = Page(self.driver, self.wait_time)

    def __del__(self):
        """Class destructor."""
        self.delete()

    def delete(self):
        """Webdriver destructor."""
        self.wait = None
        try:
            self.driver.quit()
        except:
            pass

    def run_on(self, driver_type, pasta_user=None, capabilities={}):
        """Webdriver activation.

        driver_type (string): web browser type
        pasta_user (PastaSauce): optional API access for saucelabs
        capabilities (dict): browser settings; copy object to avoid overwrite
            Defaults:
                DesiredCapabilities.ANDROID.copy()
                DesiredCapabilities.CHROME.copy()
                DesiredCapabilities.EDGE.copy()
                DesiredCapabilities.FIREFOX.copy()
                DesiredCapabilities.HTMLUNIT.copy()
                DesiredCapabilities.HTMLUNITWITHJS.copy()
                DesiredCapabilities.INTERNETEXPLORER.copy()
                DesiredCapabilities.IPAD.copy()
                DesiredCapabilities.IPHONE.copy()
                DesiredCapabilities.ORERA.copy()
                DesiredCapabilities.PHANTOMJS.copy()
                DesiredCapabilities.SAFARI.copy()
            Keys:
                platform
                browserName
                version
                javascriptEnabled
        wait (int): standard time, in seconds, to wait for Selenium commands
        opera_driver (string): Chromium location
        """
        driver = driver_type if driver_type is not None else 'chrome'
        pasta = pasta_user if pasta_user is not None else self.pasta
        try:
            return {
                'firefox': lambda: webdriver.Firefox(),
                'chrome': lambda: webdriver.Chrome(),
                'ie': lambda: webdriver.Ie(),
                'opera': lambda: self.start_opera(self.opera_driver),
                'phantomjs': lambda: webdriver.PhantomJS(),
                # 'safari': lambda: webdriver.Safari(),
                'saucelabs': lambda: webdriver.Remote(
                    command_executor=(
                        'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' %
                        (pasta.get_user(), pasta.get_access_key())),
                    desired_capabilities=self.capabilities
                ),
            }[driver]()
        except WebDriverException as err:
            raise FileNotFoundError(err)
        except Exception as err:
            raise WebDriverTypeException(
                msg='Unknown WebDriver type: "%s"' % driver,
                err=err.__traceback__
            )

    def start_opera(self, location):
        """Opera initiator."""
        webdriver_service = service.Service(location)
        webdriver_service.start()
        return webdriver.Remote(
            webdriver_service.service_url,
            DesiredCapabilities.OPERA.copy()
        )

    def change_wait_time(self, new_wait):
        """Change the max action wait time."""
        if new_wait <= 0:
            raise ValueError('Wait time must be 1 or higher.')
        self.driver.implicitly_wait(new_wait)
        self.wait = WebDriverWait(self.driver, new_wait)
        self.wait_time = new_wait

    def date_string(self, day_delta=0, str_format='%m/%d/%Y'):
        """System date format for Tutor."""
        return (datetime.date.today() + datetime.timedelta(days=day_delta)). \
            strftime(str_format)

    def get(self, url):
        """Return the current URL."""
        self.driver.get(url)
        self.page.wait_for_page_load()

    def get_window_size(self, dimension=None):
        """Return the current window dimensions."""
        get_size = self.driver.get_window_size()
        if dimension is None:
            return get_size
        if dimension not in get_size:
            raise IndexError('Unknown dimension: %s' % dimension)
        return get_size[dimension]

    def sleep(self, seconds=1):
        """Stop execution for the specified time in seconds."""
        sleep(seconds)

    def find(self, by, value):
        """Find element."""
        return self.driver.find_element(by=by, value=value)

    def find_all(self, by, value):
        """Find elements."""
        return self.driver.find_elements(by=by, value=value)


class WebDriverTypeException(WebDriverException):
    """Exception for unknown WebDriver types."""

    def __init__(self, msg, err):
        """Exception initializer."""
        self.msg = msg
        self.__traceback__ = err

    def __str__(self):
        """String representation of the exception."""
        return repr(self.msg, self.__traceback__)


class User(Helper):
    """User parent class."""

    CONDENSED_WIDTH = Helper.CONDENSED_WIDTH
    DEFAULT_WAIT_TIME = Helper.DEFAULT_WAIT_TIME

    def __init__(self, username, password, site, email=None,
                 email_username=None, email_password=None,
                 driver_type='chrome',
                 capabilities=DesiredCapabilities.CHROME.copy(),
                 pasta_user=None, wait_time=DEFAULT_WAIT_TIME,
                 opera_driver='', **kwargs):
        """
        Base user constructor.

        username (string): website username
        password (string): website password
        site (string): website URL
        driver_type (string): web browser type
        pasta_user (PastaSauce): optional API access for saucelabs
        capabilities (dict): browser settings; copy object to avoid overwrite
            Defaults:
                DesiredCapabilities.ANDROID.copy()
                DesiredCapabilities.CHROME.copy()
                DesiredCapabilities.EDGE.copy()
                DesiredCapabilities.FIREFOX.copy()
                DesiredCapabilities.HTMLUNIT.copy()
                DesiredCapabilities.HTMLUNITWITHJS.copy()
                DesiredCapabilities.INTERNETEXPLORER.copy()
                DesiredCapabilities.IPAD.copy()
                DesiredCapabilities.IPHONE.copy()
                DesiredCapabilities.ORERA.copy()
                DesiredCapabilities.PHANTOMJS.copy()
                DesiredCapabilities.SAFARI.copy()
            Keys:
                platform
                browserName
                version
                javascriptEnabled
        wait (int): standard time, in seconds, to wait for Selenium commands
        opera_driver (string): Chromium location
        """
        self.username = username
        self.password = password
        parse = list(
            urlparse(
                site if urlparse(site).scheme
                else '%s%s' % ('//', site)
            )
        )
        parse[0] = b'https'
        for index, value in enumerate(parse):
            parse[index] = value.decode('utf-8') if isinstance(value, bytes) \
                else value
        parse = ParseResult(*parse)
        self.url = parse.geturl()
        self.email = email
        self.email_username = email_username
        self.email_password = email_password
        super(User, self).__init__(driver_type=driver_type,
                                   capabilities=capabilities,
                                   pasta_user=pasta_user,
                                   wait_time=wait_time,
                                   opera_driver=opera_driver)

    def login(self, url=None, username=None, password=None):
        """
        Tutor login control.

        If parameters are not passed, login using the class values.
        Branching to deal with standard or compact screen widths

        username (string): website username
        password (string): website password
        url (string): website URL
        """
        username = self.username if username is None else username
        password = self.password if password is None else password
        url_address = self.url if url is None else url
        # open the URL
        self.get(url_address)
        self.page.wait_for_page_load()
        if 'tutor' in url_address:
            # check to see if the screen width is normal or condensed
            if self.driver.get_window_size()['width'] <= self.CONDENSED_WIDTH:
                # get small-window menu toggle
                is_collapsed = self.driver.find_element(
                    By.XPATH,
                    '//button[contains(@class,"navbar-toggle")]'
                )
                # check if the menu is collapsed and, if yes, open it
                if('collapsed' in is_collapsed.get_attribute('class')):
                    is_collapsed.click()
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.LINK_TEXT, 'Login')
                )
            ).click()
            self.page.wait_for_page_load()
        src = self.driver.page_source
        text_located = re.search(r'openstax', src.lower()) is not None
        self.sleep(1)
        if not text_located:
            raise self.LoginError('Non-OpenStax URL: %s' %
                                  self.driver.current_url)
        # enter the username and password
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.username if username is None else username)
        self.driver.find_element(By.ID, 'password'). \
            send_keys(self.password if password is None else password)
        # click on the sign in button
        self.driver.find_element(
            By.XPATH, '//button[text()="Sign in"]'
        ).click()
        self.page.wait_for_page_load()

    def logout(self):
        """Logout control."""
        url_address = self.driver.current_url
        if 'tutor' in url_address:
            self.tutor_logout()
        elif 'accounts' in url_address:
            self.accounts_logout()
        else:
            raise HTTPError('Not an OpenStax URL')

    def goto_course_list(self):
        """Go to the course picker."""
        try:
            self.wait.until(
                expect.presence_of_element_located(
                    (By.ID, 'react-root-container')
                )
            )
            if 'tutor' in self.driver.current_url:
                self.driver.find_element(
                    By.XPATH, '//a[contains(@href,"dashboard")]'
                ).click()
                self.page.wait_for_page_load()
            else:
                raise HTTPError('Not currently on an OpenStax Tutor webpage:' +
                                '%s' % self.driver.current_url)
        except Exception as ex:
            raise ex

    def open_user_menu(self):
        """
        Hamburger (user) menu opener.

        ToDo: branching to handle if a toggle is already open
        """
        if self.get_window_size('width') <= self.CONDENSED_WIDTH:
            # compressed window display on Tutor
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.CLASS_NAME, 'navbar-toggle')
                )
            ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'dropdown-toggle')
            )
        ).click()

    def tutor_logout(self):
        """Tutor logout helper."""
        self.open_user_menu()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[@aria-label="Sign out"]')
            )
        ).click()
        self.page.wait_for_page_load()

    def accounts_logout(self):
        """OS Accounts logout helper."""
        self.driver.find_element(By.LINK_TEXT, 'Sign out').click()
        self.page.wait_for_page_load()

    def select_course(self, title=None, appearance=None):
        """Select course."""
        if 'dashboard' not in self.driver.current_url:
            self.goto_course_list()
            self.page.wait_for_page_load()
        if title:
            uses_option = 'title'
            course = title
        elif appearance:
            uses_option = 'appearance'
            course = appearance.lower()
        else:
            raise self.LoginError('Unknown course selection "%s"' %
                                  title if title else appearance)
        self.wait.until(
            expect.element_to_be_clickable(
                (
                    By.XPATH, '//div[@data-%s="%s"]//a' %
                    (uses_option, course)
                )
            )
        ).click()
        self.page.wait_for_page_load()

    def view_reference_book(self):
        """Access the reference book."""
        try:
            self.driver.find_element(
                By.XPATH, '//div/a[contains(@class,"view-reference-guide")]'
            ).click()
            return
        except:
            pass
        self.open_user_menu()
        self.driver.find_element(
            By.XPATH, '//li/a[contains(@class,"view-reference-guide")]'
        ).click()


class LoginError(Exception):
    """Login error exception."""

    def __init__(self, value):
        """Exception initializer."""
        self.value = value

    def __str__(self):
        """Return string of the exception text."""
        return repr(self.value)


class Teacher(User):
    """User extention for teachers."""

    CONDENSED_WIDTH = User.CONDENSED_WIDTH
    DEFAULT_WAIT_TIME = User.DEFAULT_WAIT_TIME

    def __init__(self, username=None, password=None, site=None, email=None,
                 email_username=None, email_password=None, use_env_vars=False):
        """Teacher initialization with User pass-through."""
        if use_env_vars:
            username = os.environ['TEACHER_USER']
            password = os.environ['TEACHER_PASSWORD']
            site = os.environ['SERVER_URL']
            email = os.environ['TEST_EMAIL_ACCOUNT']
            email_username = os.environ['TEST_EMAIL_USER']
            email_password = os.environ['TEST_EMAIL_PASSWORD']
        super(Teacher, self).__init__(username, password, site, email,
                                      email_username, email_password)

    def add_assignment(self, assignment, args):
        """Add an assignment."""
        assign = Assignment()
        assign.add[assignment](
            driver=self.driver,
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
        """Alter an existing assignment."""
        assign = Assignment()
        assign.edit[assignment](
            driver=self.driver,
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
        """Delete an existing assignment (if available)."""
        assign = Assignment()
        assign.remove[assignment](
            driver=self.driver,
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
        """Go to a specific user menu item."""
        print('Enter: goto_menu_item')
        if 'courses' in self.driver.current_url:
            self.open_user_menu()
            self.wait.until(
                expect.element_to_be_clickable(
                    (By.LINK_TEXT, item)
                )
            ).click()
            self.page.wait_for_page_load()
        print('Exit: goto_menu_item')

    def goto_calendar(self):
        """Return the teacher to the calendar dashboard."""
        print('Enter: goto_calendar')
        try:
            self.driver.find_element(
                By.XPATH, '//a[contains(@href,"calendar")]'
            ).click()
            self.page.wait_for_page_load()
        except:
            try:
                self.driver.find_element(
                    By.XPATH, '//a[contains(@class,"navbar-brand")]'
                ).click()
                self.page.wait_for_page_load()
            except:
                pass
        print('Exit: goto_calendar')

    def goto_performance_forecast(self):
        """Access the performance forecast page."""
        print('Enter: goto_performance_forecast')
        self.goto_menu_item('Performance Forecast')
        timer = 0
        while timer < 10:
            try:
                self.wait.until(
                    expect.visibility_of_element_located(
                        (By.CLASS_NAME, 'guide-container')
                    )
                )
                timer = 10
            except:
                timer = timer + 1
        print('Exit: goto_performance_forecast')

    def goto_student_scores(self):
        """Access the student scores page."""
        print('Enter: goto_student_scores')
        self.goto_menu_item('Student Scores')
        print('Exit: goto_student_scores')

    def goto_course_roster(self):
        """Access the course roster page."""
        print('Enter: goto_course_roster')
        self.goto_menu_item('Course Roster')
        print('Exit: goto_course_roster')

    def add_course_section(self, section_name):
        """Add a section to the course."""
        print('Enter: add_course_section')
        if 'settings' not in self.driver.current_url:
            self.goto_course_roster()
        self.driver.find_element(
            By.XPATH, '//button[i[contains(@class,"fa-plus")]]'
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"teacher-edit-period-form")]' +
                 '//input[@type="text"]')
            )
        ).send_keys(section_name)
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"-edit-period-confirm")]')
            )
        ).click()
        print('Exit: add_course_section')

    def get_enrollment_code(self, section_name):
        """Return the enrollment phrase for a class section."""
        print('Enter: get_enrollment_code')
        if 'settings' not in self.driver.current_url:
            self.goto_course_roster()
        self.driver.find_element(
            By.XPATH, '//a[span[@class="tab-item-period-name" ' +
            'and text()="%s"]]' % section_name
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.CLASS_NAME, 'show-enrollment-code')
            )
        ).click()
        return self.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'code')
            )
        ).text
        print('Exit: get_enrollment_code')


class Student(User):
    """User extention for students."""

    CONDENSED_WIDTH = User.CONDENSED_WIDTH
    DEFAULT_WAIT_TIME = User.DEFAULT_WAIT_TIME

    def __init__(self, username=None, password=None, site=None, email=None,
                 email_username=None, email_password=None, use_env_vars=False):
        """Student initialization with User pass-through."""
        if use_env_vars:
            username = os.environ['STUDENT_USER']
            password = os.environ['STUDENT_PASSWORD']
            site = os.environ['SERVER_URL']
            email = os.environ['TEST_EMAIL_ACCOUNT']
            email_username = os.environ['TEST_EMAIL_USER']
            email_password = os.environ['TEST_EMAIL_PASSWORD']
        super(Student, self).__init__(username, password, site, email,
                                      email_username, email_password)

    def work_assignment(self):
        """Work an assignment.

        ToDo: all
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    def goto_past_work(self):
        """View work for previous weeks.

        ToDo: all
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    def goto_performance_forecast(self):
        """View the student performance forecast.

        ToDo: all
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    def practice(self):
        """Complete a set of 5 practice problems.

        ToDo: all
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


class Admin(User):
    """User extention for administrators."""

    CONDENSED_WIDTH = User.CONDENSED_WIDTH
    DEFAULT_WAIT_TIME = User.DEFAULT_WAIT_TIME

    def __init__(self, username=None, password=None, site=None, email=None,
                 email_username=None, email_password=None, use_env_vars=False):
        """Administrator initialization with User pass-through."""
        if use_env_vars:
            username = os.environ['ADMIN_USER']
            password = os.environ['ADMIN_PASSWORD']
            site = os.environ['SERVER_URL']
            email = os.environ['TEST_EMAIL_ACCOUNT']
            email_username = os.environ['TEST_EMAIL_USER']
            email_password = os.environ['TEST_EMAIL_PASSWORD']
        super(Admin, self).__init__(username, password, site, email,
                                    email_username, email_password)

    def goto_admin_control(self):
        """Access the administrator controls."""
        self.wait.until(
            expect.visibility_of_element_located(
                (
                    By.XPATH, '%s%s' %
                    ('//li[contains(@class,"-hamburger-menu")]/',
                     'a[@type="button"]')
                )
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Admin')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Admin Console"]')
            )
        )

    def goto_courses(self):
        """Access the course admin control."""
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Admin Console"]')
                )
            )
        except:
            self.goto_admin_control()
        organization = self.wait.until(
            expect.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        )
        if 'open' not in organization.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            organization.click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Courses')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Courses"]')
            )
        )

    def goto_ecosystems(self):
        """Access the ecosystem admin control."""
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Admin Console"]')
                )
            )
        except:
            self.goto_admin_control()
        content = self.wait.until(
            expect.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        )
        if 'open' not in content.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            content.click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Ecosystems')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Ecosystems"]')
            )
        )


class ContentQA(User):
    """User extention for content users."""

    CONDENSED_WIDTH = User.CONDENSED_WIDTH
    DEFAULT_WAIT_TIME = User.DEFAULT_WAIT_TIME

    def __init__(self, username=None, password=None, site=None, email=None,
                 email_username=None, email_password=None, use_env_vars=False):
        """Content analyst initialization with User pass-through."""
        if use_env_vars:
            username = os.environ['CONTENT_USER']
            password = os.environ['CONTENT_PASSWORD']
            site = os.environ['SERVER_URL']
            email = os.environ['TEST_EMAIL_ACCOUNT']
            email_username = os.environ['TEST_EMAIL_USER']
            email_password = os.environ['TEST_EMAIL_PASSWORD']
        super(ContentQA, self).__init__(username, password, site, email,
                                        email_username, email_password)


if __name__ == '__main__':
    # execute if run as a script
    initialization = Helper