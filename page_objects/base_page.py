import allure

import selenium
from allure_commons.types import AttachmentType
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger import logger_events


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def take_screenshot(self, name: str = "screenshot") -> None:
        """Делает скриншот и прикрепляет к Allure-отчету"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=AttachmentType.PNG,
        )

    def save_page_source(self, name: str = "page_source") -> None:
        """Сохраняет исходный код страницы в отчет"""
        allure.attach(
            self.driver.page_source, name=name, attachment_type=AttachmentType.HTML
        )

    def save_current_url(self, name: str = "current_url") -> None:
        """Сохраняет текущий URL в отчет"""
        allure.attach(
            self.driver.current_url, name=name, attachment_type=AttachmentType.TEXT
        )

    def save_debug_info_on_failure(self) -> None:
        """Сохраняет всю отладочную информацию при падении теста"""
        self.take_screenshot("screenshot_on_failure")
        self.save_page_source()
        self.save_current_url()

    def open(self, base_url, path=""):
        logger_events.log_ui_event(f"{base_url + path}")
        self.driver.get(base_url + path)

    def click(self, locator):
        logger_events.log_ui_event(locator)
        element = self.driver.find_element(*locator)
        element.click()

    def send_keys(self, keys, locator):
        logger_events.log_ui_event(locator)
        element = self.driver.find_element(*locator)
        element.send_keys(keys)

    def clear(self, locator):
        logger_events.log_ui_event(locator)
        element = self.driver.find_element(*locator)
        element.clear()

    def get_text(self, locator):
        logger_events.log_ui_event(locator)
        element = self.driver.find_element(*locator)
        return element.text()

    def is_visible(self, locator):
        try:
            logger_events.log_ui_event(locator)
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
        except selenium.common.exceptions.TimeoutException:
            raise AssertionError

    def is_presence(self, locator):
        try:
            logger_events.log_ui_event(locator)
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator)
            )
        except selenium.common.exceptions.TimeoutException:
            raise AssertionError

    def is_clickable(self, locator):
        try:
            logger_events.log_ui_event(locator)
            return WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
            )
        except selenium.common.exceptions.TimeoutException:
            raise AssertionError

    def find_element(self, by, value):
        try:
            logger_events.log_ui_event((by, value))
            return self.driver.find_element(by, value)
        except NoSuchElementException as e:
            raise AssertionError(e.msg)

    def find_elements(self, by, value):
        try:
            logger_events.log_ui_event((by, value))
            return self.driver.find_elements(by, value)
        except NoSuchElementException as e:
            raise AssertionError(e.msg)
