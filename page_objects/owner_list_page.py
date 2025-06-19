import time
import allure

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

from page_objects.base_page import BasePage


class OwnerListPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Ввод имени существующего владельца")
    def set_lastname_owner_to_search_field(self, last_name):
        self.send_keys(last_name, (By.ID, "lastName"))

    @allure.step("Нажатие на копку подтверждения поиска владельца")
    def click_find_owner_button(self):
        button = self.find_element(By.CSS_SELECTOR, '[type="submit"]')
        button.click()

    @allure.step("Выбор владельца")
    def click_owner_name_button(self, owner_name):
        max_attempts = 5
        attempt = 0

        while attempt < max_attempts:
            try:
                button = self.is_presence(
                    (By.XPATH, f'//a[contains(text(), "{owner_name}")]')
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                    button,
                )
                button = self.is_clickable(
                    (By.XPATH, f'//a[contains(text(), "{owner_name}")]')
                )
                button.click()
                return

            except (AssertionError, StaleElementReferenceException):
                self.driver.execute_script("window.scrollBy(0, 300);")
                attempt += 1
                time.sleep(1)

        raise AssertionError(
            f"Не удалось найти или кликнуть на элемент с именем '{owner_name}' после {max_attempts} попыток"
        )

    @allure.step("Нажимаю на кнопку 'Owners' в заголовке")
    def click_owners_button(self):
        owners = self.find_element(By.XPATH, '//a[contains(text(), "Owners")]')
        owners.click()

    @allure.step("Нажимаю на кнопку поиска владельца в drop_down menu")
    def click_search_button(self):
        owners = self.find_element(By.CSS_SELECTOR, '[href="/petclinic/owners"]')
        owners.click()

    @allure.step("Таблица владельцев отображается")
    def owner_table_is_visible(self):
        return self.is_visible((By.ID, "ownersTable"))

    @allure.step("Заголовок на странице отображается")
    def owner_header_is_visible(self):
        return self.is_visible((By.XPATH, '//h2[contains(text(), "Owners")]'))

    @allure.step("Искомый владелец отображается")
    def owner_in_table_is_visible(self, owner_name):
        max_attempts = 5
        attempt = 0

        while attempt < max_attempts:
            try:
                element = self.is_presence(
                    (By.XPATH, f'//a[contains(text(), "{owner_name}")]')
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                    element,
                )
                if element.is_displayed():
                    return True

            except (
                AssertionError,
                NoSuchElementException,
                StaleElementReferenceException,
            ):
                self.driver.execute_script("window.scrollBy(0, 300);")
                attempt += 1
                time.sleep(1)

        raise AssertionError(
            f"Не удалось найти элемент с именем '{owner_name}' после {max_attempts} попыток"
        )

    @allure.step("Получение владельцев по имени")
    def owners_in_table_by_name(self, owner_name):
        return self.find_elements(By.XPATH, f'//a[contains(text(), "{owner_name}")]')
