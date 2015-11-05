import random
import string
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
# from datetime import date


class Assignment(object):
    '''
    Shortcut functions to add, edit, and delete assignments
    '''
    READING = 'reading'
    HOMEWORK = 'homework'
    EXTERNAL = 'external'
    EVENT = 'event'
    REVIEW = 'review'

    WAIT_TIME = 15

    TUTOR_SELECTIONS = 'tutor'

    PUBLISH = 'publish'
    CANCEL = 'cancel'
    DRAFT = 'draft'

    def __init__(self):
        '''
        Provide a switch-style dictionary to add assignments
        '''
        self.add = {
            Assignment.READING:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.add_new_reading(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    readings=reading_list,
                    status=state)
            ),
            Assignment.HOMEWORK:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.add_new_homework(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    problems=problems,
                    status=state)
            ),
            Assignment.EXTERNAL:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.add_new_external(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    assignment_url=url,
                    status=state)
            ),
            Assignment.EVENT:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.add_new_event(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    status=state)
            ),
            Assignment.REVIEW:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.add_new_review(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    assessments=problems,
                    assignment_url=url,
                    status=state)
            ),
        }
        self.edit = {
            Assignment.READING:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.change_reading(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    readings=reading_list,
                    status=state)
            ),
            Assignment.HOMEWORK:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.change_homework(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    problems=problems,
                    status=state)
            ),
            Assignment.EXTERNAL:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.change_external(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    assignment_url=url,
                    status=state)
            ),
            Assignment.EVENT:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.change_event(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    status=state)
            ),
            Assignment.REVIEW:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.change_review(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    assessments=problems,
                    assignment_url=url,
                    status=state)
            ),
        }
        self.remove = {
            Assignment.READING:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.delete_reading(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    readings=reading_list,
                    status=state)
            ),
            Assignment.HOMEWORK:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.delete_homework(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    problems=problems,
                    status=state)
            ),
            Assignment.EXTERNAL:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.delete_external(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    assignment_url=url,
                    status=state)
            ),
            Assignment.EVENT:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.delete_event(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    status=state)
            ),
            Assignment.REVIEW:
            (
                lambda driver, name, description, periods, reading_list, state,
                problems, url:
                self.delete_review(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    assessments=problems,
                    assignment_url=url,
                    status=state)
            ),
        }

    @classmethod
    def rword(cls, length):
        '''
        Return a <length>-character random string
        '''
        return ''.join(random.choice(string.ascii_lowercase)
                       for i in range(length))

    def open_assignment_menu(self, driver):
        '''
        Open the Add Assignment menu if it is closed
        '''
        try:
            assignment_menu = driver.find_element(
                By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
            # if the Add Assignment menu is not open
            if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                    get_attribute('class'):
                assignment_menu.click()
        except:
            return

    def assign_periods(self, driver, periods):
        '''
        Assign open and close dates
        '''
        # assign the same dates for all periods
        if 'all' in periods:
            opens_on, closes_on = periods['all']
            time.sleep(1)
            open_xpath = '//div[contains(@class,"-assignment-open-date")]' + \
                         '//input[@class="datepicker__input"]'
            close_xpath = '//div[contains(@class,"-assignment-due-date")]' + \
                          '//input[@class="datepicker__input"]'
            driver.find_element(By.XPATH, open_xpath).clear()
            driver.find_element(By.XPATH, open_xpath).send_keys(opens_on)
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, 'assign-to-label').click()
            time.sleep(1)
            driver.find_element(By.XPATH, close_xpath).clear()
            driver.find_element(By.XPATH, close_xpath).send_keys(closes_on)
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, 'assign-to-label').click()
            return
        # or set the dates for each period: {period: (open, close)}
        count = 0
        last = len(periods)
        for period in periods:
            count += 1
            if count > last:
                break
                if periods[period] is 'all' or period is 'skip':
                    continue
                opens_on, closes_on = periods[period]
                driver.find_element(
                    By.XPATH,
                    '//input[@id="period-toggle-%s"]' % count +
                    '/../following-sibling::div' +
                    '//input[contains(@class,"picker")]'). \
                    send_keys(opens_on)
                driver.find_element(
                    By.XPATH,
                    '//input[@id="period-toggle-%s"]' % count +
                    '/../following-sibling::div/following-sibling::div' +
                    '//input[contains(@class,"picker")]'). \
                    send_keys(closes_on)

    def select_status(self, driver, status):
        if status is self.PUBLISH:
            driver.find_element(
                By.XPATH,
                '//button[contains(@class,"-publish")]'). \
                click()
        elif status is self.DRAFT:
            driver.find_element(
                By.XPATH,
                '//button[contains(@class," -save")]'). \
                click()
        else:
            driver.find_element(
                By.XPATH,
                '//button[contains(@aria-role,"close"'). \
                click()
            wait = WebDriverWait(driver, Assignment.WAIT_TIME)
            wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//button[contains(@class,"ok")]')
                )
            ).click()

    def open_chapter_list(self, driver, chapter):
        '''
        Open the reading chapter list
        '''
        data_chapter = driver.find_element(
            By.XPATH,
            '//h2[contains(@data-chapter-section,"%s")]/a' % chapter
        )
        if not bool(data_chapter.get_attribute('aria_expanded')):
            data_chapter.click()

    def select_sections(self, driver, chapters):
        '''
        Select the sections and chapters
        '''
        for section in chapters:
            if "ch" in section:  # select the whole chapter
                print('Adding chapter: ' + section)
                chapter = driver.find_element(
                    By.XPATH,
                    '//h2[@data-chapter-section="%s"]' % section[2:] +
                    '//input[contains(@id,"chapter-checkbox-")]'
                )
                if not chapter.is_selected():
                    chapter.click()
            else:  # select an individual section
                print('Adding section: ' + section)
                self.open_chapter_list(driver, section.split('.')[0])
                time.sleep(0.5)
                wait = WebDriverWait(driver, Assignment.WAIT_TIME)
                marked = wait.until(
                    expect.visibility_of_element_located(
                        (By.XPATH,
                         ('//span[contains(@data-chapter-section' +
                          ',"{s}") and text()="{s}"]').format(s=section) +
                         '/preceding-sibling::span/input')
                    )
                )
                if not marked.is_selected():
                    marked.click()

    def add_new_reading(self, driver, title, description, periods, readings,
                        status):
        '''
        Add a new reading assignment

        driver:      WebDriver - Selenium WebDriver instance
        title:       string    - assignment title
        description: string    - assignment description or additional
                                 instructions
        periods:     dict      - <key>:   string <period name> OR 'all'
                                 <value>: tuple  (<open date>, <close date>)
                                          date format is 'MM/DD/YYYY'
        readings:    [string]  - chapter and section numbers to include in the
                                 assignment; chapter numbers are prefixed with
                                 'ch'
        status:      string    - 'publish', 'cancel', or 'draft'
        '''
        self.open_assignment_menu(driver)
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, 'Add Reading').click()
        time.sleep(1)
        wait = WebDriverWait(driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'panel-body')
            )
        )
        wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'reading-title')
            )
        )
        driver.find_element(By.ID, 'reading-title').send_keys(title)
        time.sleep(1)
        driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]//textarea' +
            '[contains(@class,"form-control")]'). \
            send_keys(description)
        time.sleep(1)
        self.assign_periods(driver, periods)
        time.sleep(1)
        # add reading sections to the assignment
        driver.find_element(By.ID, 'reading-select').click()
        time.sleep(1)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"select-reading-' +
                 'dialog")]')
            )
        )
        time.sleep(1)
        self.select_sections(driver, readings)
        time.sleep(1)
        driver.find_element(By.XPATH,
                            '//button[text()="Add Readings"]').click()
        time.sleep(3)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Publish"]')
            )
        )
        self.select_status(driver, status)
        time.sleep(5)

    def add_new_homework(self, driver, title, description, periods, problems,
                         status):
        '''
        Add a new homework assignment

        driver:      WebDriver - Selenium WebDriver instance
        title:       string    - assignment title
        description: string    - assignment description or additional
                                 instructions
        periods:     dict      - <key>:   string <period name> OR 'all'
                                 <value>: tuple  (<open date>, <close date>)
                                          date format is 'MM/DD/YYYY'
        problems:    dict      - <key>:   string '<chapter.section>' or 'tutor'
                               - <value>: [string] Ex-IDs
                                          int use first <int> exercises
                                              available
                                          (int, int) between <min> and <max>
                                              exercises
                                          'all' select all exercises in a
                                              section
                                          int 'tutor' takes 2, 3, or 4
                                              default: 3
        status:      string    - 'publish', 'cancel', or 'draft'
        '''
        self.open_assignment_menu(driver)
        driver.find_element(By.LINK_TEXT, 'Add Homework').click()
        wait = WebDriverWait(driver, Assignment.WAIT_TIME)
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"homework-plan")]')
            )
        )
        driver.find_element(By.ID, 'reading-title').send_keys(title)
        driver.find_element(
            By.XPATH,
            '//div[contains(@class,"assignment-description")]' +
            '//textarea[contains(@class,"form-control")]'). \
            send_keys(description)
        self.assign_periods(driver, periods)
        driver.find_element(By.ID, 'problems-select').click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[text()="Add Problems"]')
            )
        )
        self.select_sections(driver, problems)
        driver.find_element(By.XPATH, '//button[text()="Show Problms"]'). \
            click()
        for section in problems:
            if section is 'tutor':
                tutor_picks = driver.find_element(
                    By.XPATH, '//div[@class="tutor-selections"]//h2')
                current = int(tutor_picks.text)
                change = current - problems[section]
                if change != 0:
                    increase = driver.find_element(
                        By.XPATH,
                        '//div[@class="tutor-selections"]' +
                        '//button[contains(@class,"-move-exercise-down")]'
                    )
                    decrease = driver.find_element(
                        By.XPATH,
                        '//div[@class="tutor-selections"]' +
                        '//button[contains(@class,"-move-exercise-up")]'
                    )
                    while change < 0:
                        change += 1
                        increase.click()
                    while change > 0:
                        change -= 1
                        decrease.click()
            # elif
        # #####
        self.select_status(driver, status)

    def add_new_external(self, driver, title, description, periods,
                         assignment_url, status):
        '''

        '''
        raise NotImplementedError

    def add_new_event(self, driver, title, description, periods, status):
        '''

        '''
        raise NotImplementedError

    def add_new_review(self, driver, title, description, periods, assessments,
                       assignment_url, status):
        '''

        '''
        raise NotImplementedError

    def change_reading(self, driver, title, description, periods, readings,
                       status):
        '''

        '''
        raise NotImplementedError

    def change_homework(self, driver, title, description, periods, problems,
                        status):
        '''

        '''
        raise NotImplementedError

    def achange_external(self, driver, title, description, periods,
                         assignment_url, status):
        '''

        '''
        raise NotImplementedError

    def change_event(self, driver, title, description, periods, status):
        '''

        '''
        raise NotImplementedError

    def change_review(self, driver, title, description, periods, assessments,
                      assignment_url, status):
        '''

        '''
        raise NotImplementedError

    def delete_reading(self, driver, title, description, periods, readings,
                       status):
        '''

        '''
        raise NotImplementedError

    def delete_homework(self, driver, title, description, periods, problems,
                        status):
        '''

        '''
        raise NotImplementedError

    def delete_external(self, driver, title, description, periods,
                        assignment_url, status):
        '''

        '''
        raise NotImplementedError

    def delete_event(self, driver, title, description, periods, status):
        '''

        '''
        raise NotImplementedError

    def delete_review(self, driver, title, description, periods, assessments,
                      assignment_url, status):
        '''

        '''
        raise NotImplementedError
