import allure

from page_objects.base_page import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Welcome to Petclinic текст отображается")
    def welcome_to_petclinic_text_is_visible(self):
        return self.is_visible((By.CSS_SELECTOR, 'h1.title'))

    @allure.step("Welcome текст отображается")
    def welcome_text_is_visible(self):
        return self.is_visible((By.XPATH, '//h2[contains(text(), "Welcome")]'))

    @allure.step("Nav_bar отображается")
    def nav_bar_is_visible(self):
        return self.is_visible((By.CSS_SELECTOR, '[class="navbar navbar-default"]'))

    @allure.step("Pets.png отображается")
    def pets_png_is_visible(self):
        return self.is_visible((By.CSS_SELECTOR, '[src="./assets/images/pets.png"]'))
