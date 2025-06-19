import allure

from page_objects.base_page import BasePage
from selenium.webdriver.common.by import By


class OwnerInformationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Нажатие на кнопку редактирования владельца")
    def click_edit_owner_button(self):
        button = self.find_element(By.XPATH, '//button[contains(text(), "Edit Owner")]')
        button.click()

    @allure.step("Нажатие на кнопку возврата к списку владельцев")
    def click_back_button(self):
        button = self.find_element(By.XPATH, '//button[contains(text(), "Back")]')
        button.click()

    @allure.step("Получение информации о владельце")
    def get_owner_information(self):
        self.is_visible((By.XPATH, '//h2[contains(text(), "Owner Information")]'))
        tables = self.find_elements(By.CSS_SELECTOR, "div .table.table-striped")
        owner_information_table = tables[0]
        return owner_information_table.text

    @allure.step("Получение информации о питомцах")
    def get_pet_information(self):
        tables = self.find_elements(By.CSS_SELECTOR, "div .table.table-striped")
        pet_information_table = tables[1]
        return pet_information_table.text

    @allure.step("Таблица с питомцами отображается")
    def pet_table_is_visible(self):
        tables = self.find_elements(By.CSS_SELECTOR, "div .table.table-striped")
        pet_information_table = tables[1]
        return len(pet_information_table.text) > 0

    @allure.step("Информация о питомцах отображается")
    def pet_header_is_visible(self):
        return self.is_visible((By.XPATH, '//h2[contains(text(), "Pets and Visits")]'))

    @allure.step("Нажатие на кнопку удаления питомца")
    def click_delete_pet_button(self):
        button = self.find_element(By.XPATH, '//button[contains(text(), "Delete Pet")]')
        button.click()

    @allure.step("Получение информации и визитах в клинику")
    def get_visit_information(self):
        tables = self.find_elements(By.CSS_SELECTOR, "div .table.table-striped")
        visit_information_table = tables[1]
        return visit_information_table.text
