import pytest
import allure

from page_objects.home_page import HomePage


@pytest.mark.nondestructive
@pytest.mark.test
@allure.title("Проверка главной страницы")
def test_home_page(driver, base_url):
    home_page = HomePage(driver)
    home_page.open(base_url)

    assert home_page.nav_bar_is_visible()
    assert home_page.welcome_to_petclinic_text_is_visible()
    assert home_page.pets_png_is_visible()
    assert home_page.welcome_text_is_visible()
    assert False
