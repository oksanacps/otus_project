import pytest
import allure

from src.http_client.base_request import BaseRequest
from test_data.url_data import BASE_URL_PETCLINIC


@pytest.fixture(scope='module')
@allure.step("Получение base_url, прокидывание заголовков")
def get_request_instance():
    headers = {'Content-Type': 'application/json',
               'accept': 'application/json'}
    request = BaseRequest(BASE_URL_PETCLINIC, headers)
    return request
