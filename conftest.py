import json
import random
import re
import pytest
import logging
import allure

from faker import Faker

from helpers import helpers
from src.database.my_sql.db_client import MySqlDbClient
from db_steps import db_steps
from src.http_client.base_request import BaseRequest
from test_data.url_data import BASE_URL_PETCLINIC

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def pytest_addoption(parser):
    parser.addoption("--db-host", action="store", default="localhost")
    parser.addoption("--db-port", action="store", default=3306)
    parser.addoption("--db-user", action="store", default="petclinic")
    parser.addoption("--db-password", action="store", default="petclinic")
    parser.addoption("--db-name", action="store", default="petclinic")


@pytest.fixture(scope="session")
def db_client(request):
    db_client = MySqlDbClient(
        host=request.config.getoption("--db-host"),
        port=request.config.getoption("--db-port"),
        user=request.config.getoption("--db-user"),
        password=request.config.getoption("--db-password"),
        db=request.config.getoption("--db-name"),
    )
    assert db_client.connection.open

    yield db_client

    db_client.close()


@pytest.fixture(scope='module')
@allure.step("Получение base_url, прокидывание заголовков")
def get_request_instance():
    headers = {'Content-Type': 'application/json',
               'accept': 'application/json'}
    request = BaseRequest(BASE_URL_PETCLINIC, headers)
    return request


@pytest.fixture()
@allure.step("Создание владельца питомца")
def create_owner(db_client, generate_owner_data):
    owner_data = generate_owner_data
    owner_id = db_steps.create_owner(db_client, owner_data)

    return owner_id, owner_data


@pytest.fixture()
@allure.step("Создание владельца с питомцем")
def create_owner_with_pets(get_request_instance, db_client, generate_owner_data, create_owner, generate_pet_data):
    request = get_request_instance
    owner_id, owner_data = create_owner
    data_new_pet = generate_pet_data
    response = request.post(endpoint=f'api/owners/{owner_id}/pets', body=json.dumps(data_new_pet))
    pet_id = response.get('id')
    pet_data = helpers.get_pet_in_db(db_client, pet_id)

    assert pet_data.get('owner_id') == owner_id

    return pet_id, owner_id, owner_data, data_new_pet


@pytest.fixture()
@allure.step("Создание владельца с питомцем и визитом в клинику")
def create_owner_with_pets_visit(get_request_instance, db_client, generate_owner_data, create_owner_with_pets):
    request = get_request_instance
    pet_id, owner_id, owner_data, data_new_pet = create_owner_with_pets
    body = {
        "date": "2013-01-01",
        "description": "rabies shot"
    }
    response = request.post(endpoint=f'api/owners/{owner_id}/pets/{pet_id}/visits', body=json.dumps(body))

    assert response.get('petId') == pet_id

    return pet_id, owner_id


@pytest.fixture()
@allure.step("Очищение БД")
def cleanup_owner(request, db_client):
    """
    Фикстура для удаления владельцев питомцев после теста.
    """
    owner_to_cleanup = []

    def cleanup_owners():
        for owner_id in owner_to_cleanup:
            pets = db_steps.get_all_pets_by_owner_id(db_client, owner_id)
            for pet in pets:
                db_steps.delete_all_visits_by_pet_id(db_client, pet.get('id'))
            db_steps.delete_all_pets_by_owner_id(db_client, owner_id)
            db_steps.delete_owner(db_client, owner_id)

    request.addfinalizer(cleanup_owners)

    def add_owner_for_cleanup(owner_id):
        owner_to_cleanup.append(owner_id)

    return add_owner_for_cleanup


@pytest.fixture()
@allure.step("Генерация данных будущего владельца")
def generate_owner_data():
    """
    Фикстура для генерации случайных данных владельца питомца с помощью Faker.
    Возвращает словарь с данными владельца, обрезанными до длины, допустимой в БД:
    - firstName: varchar(30)
    - lastName: varchar(30)
    - address: varchar(255)
    - city: varchar(80)
    - telephone: varchar(10)
    """

    fake = Faker()

    firstname = fake.first_name()[:30]
    lastname = fake.last_name()[:30]
    address = fake.address().replace("\n", " ")[:255]
    city = fake.city()[:80]
    telephone = re.sub(r"[^0-9]", "", fake.phone_number())[:10]
    telephone = telephone.ljust(10, "0")  # Если цифр меньше 10, дополняем нулями

    owner_data = {
        "firstName": firstname,
        "lastName": lastname,
        "address": address,
        "city": city,
        "telephone": telephone
    }
    return owner_data


@pytest.fixture()
@allure.step("Генерация данных будущего питомца")
def generate_pet_data(db_client):
    """
    Фикстура для генерации случайных данных питомца с помощью Faker.
    Возвращает словарь с данными питомца, обрезанными до длины, допустимой в БД:
    - name: varchar(30)
    - birthDate: date
    и одним из типов существующих в БД
    """

    fake = Faker()

    name = fake.first_name()[:30]
    birthDate = fake.date_of_birth().strftime('%Y-%m-%d')

    pet_types = db_steps.get_pet_types(db_client)
    random_type = random.choice(pet_types)

    pet_data = {
        "name": name,
        "birthDate": birthDate,
        "type": {
            "name": random_type.get('name'),
            "id": random_type.get('id')
        }
    }
    return pet_data

