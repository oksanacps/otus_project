import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions

from page_objects.base_page import BasePage
from page_objects.owner_list_page import OwnerListPage


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base_url")


@pytest.fixture()
def driver(request):
    browser_name = request.config.getoption("--browser")
    exe_host = request.config.getoption("--exe_host")
    vnc = request.config.getoption("--vnc")

    if browser_name == "chrome":
        options = ChromeOptions()
    elif browser_name == "firefox":
        options = FireFoxOptions()

    selenoid_options = {
        "enableVNC": vnc,
        "browserName": browser_name,
    }

    options.set_capability("selenoid:options", selenoid_options)

    browser = webdriver.Remote(command_executor=f"http://{exe_host}:4444/wd/hub", options=options)

    # Инициализируем базовую страницу
    base_page = BasePage(browser)

    # Сохраняем base_page в browser для легкого доступа из тестов
    browser.base_page = base_page

    yield browser

    # Этот код выполнится после завершения теста
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        browser.base_page.save_debug_info_on_failure()

    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Эта функция помогает определить статус теста (упал/не упал)
    outcome = yield
    rep = outcome.get_result()

    # Устанавливаем атрибут отчета для каждого из этапов теста
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture()
def open_owner_information_page_without_pet(driver, base_url, create_owner):
    owner_id, owner_data = create_owner
    owner_name = owner_data.get('firstName') + ' ' + owner_data.get('lastName')
    owner_last_name = owner_data.get('lastName')

    open_owner_information_page(driver, base_url, owner_name, owner_last_name)

    yield owner_id, owner_data


@pytest.fixture()
def open_owner_information_page_with_pet(driver, base_url, create_owner_with_pets):
    pet_id, owner_id, owner_data, data_new_pet = create_owner_with_pets
    owner_full_name = owner_data.get('firstName') + ' ' + owner_data.get('lastName')
    owner_last_name = owner_data.get('lastName')

    open_owner_information_page(driver, base_url, owner_full_name, owner_last_name)

    yield owner_id, owner_data, data_new_pet


@pytest.fixture()
def open_owner_information_page_with_pet_and_visit(driver, base_url, create_owner_with_pets_visit):
    pet_id, owner_id, owner_data, data_new_pet, visit_data = create_owner_with_pets_visit
    owner_name = owner_data.get('firstName') + ' ' + owner_data.get('lastName')
    owner_last_name = owner_data.get('lastName')

    open_owner_information_page(driver, base_url, owner_name, owner_last_name)

    yield owner_id, owner_data, data_new_pet, visit_data


def open_owner_information_page(driver, base_url, owner_full_name, owner_last_name):
    owner_list_page = OwnerListPage(driver)

    owner_list_page.open(base_url)
    owner_list_page.click_owners_button()
    owner_list_page.click_search_button()
    owner_list_page.set_lastname_owner_to_search_field(owner_last_name)
    owner_list_page.click_find_owner_button()

    owner_list_page.click_owner_name_button(owner_full_name)
