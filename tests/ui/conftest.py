import pytest
import allure
from allure_commons.types import AttachmentType

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions

from page_objects.base_page import BasePage


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
    if request.node.rep_call.failed:
        browser.base_page.save_debug_info_on_failure()

    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Эта функция помогает определить статус теста (упал/не упал)
    outcome = yield
    rep = outcome.get_result()

    # Устанавливаем атрибут отчета для каждого из этапов теста
    setattr(item, "rep_" + rep.when, rep)
