import pytest
import allure

from page_objects.home_page import HomePage


@pytest.mark.smoke
class TestOpenHomePage:
    """ """

    @pytest.mark.nondestructive
    @allure.title("Проверка главной страницы")
    def test_home_page(self, driver, base_url):
        home_page = HomePage(driver)
        home_page.open(base_url)

        assert home_page.nav_bar_is_visible()
        assert home_page.welcome_to_petclinic_text_is_visible()
        assert home_page.pets_png_is_visible()
        assert home_page.welcome_text_is_visible()
