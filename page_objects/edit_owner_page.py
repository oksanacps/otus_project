import allure

from page_objects.base_page import BasePage
from selenium.webdriver.common.by import By


class EditOwnerPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Нажимаю на кнопку подтверждения обновления владельца")
    def click_update_owner_button(self):
        button = self.find_element(By.CSS_SELECTOR, '[type="submit"]')
        button.click()

    @allure.step("Заполнение данных владельца")
    def set_owner_data(self, first_name, last_name, address, city, telephone):
        self.clear((By.ID, 'firstName'))
        self.send_keys(first_name, (By.ID, 'firstName'))
        self.clear((By.ID, 'lastName'))
        self.send_keys(last_name, (By.ID, 'lastName'))
        self.clear((By.ID, 'address'))
        self.send_keys(address, (By.ID, 'address'))
        self.clear((By.ID, 'city'))
        self.send_keys(city, (By.ID, 'city'))
        # self.clear((By.ID, 'telephone'))    # Специально для падения теста
        self.send_keys(telephone, (By.ID, 'telephone'))

    @allure.step("Нажимаю на кнопку возврата на страницк информации о владельце")
    def click_back_button(self):
        button = self.find_element(By.XPATH, '//button[contains(text(), "Back")]')
        button.click()
