import json

from faker import Faker
import pytest
import logging

from src.database.my_sql.db_client import MySqlDbClient
from db_steps import db_steps

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


@pytest.fixture()
def create_owner(db_client, generate_owner_data):
    owner_data = generate_owner_data
    id = db_steps.create_owner(db_client, owner_data)

    return id, owner_data


@pytest.fixture()
def cleanup_owner(request, db_client):
    """
    Фикстура для удаления владельцев питомцев после теста.
    """
    owner_to_cleanup = []

    def cleanup_owners():
        for _id in owner_to_cleanup:
            db_steps.delete_owner(db_client, _id)

    request.addfinalizer(cleanup_owners)

    def add_owner_for_cleanup(_id):
        owner_to_cleanup.append(_id)

    return add_owner_for_cleanup


@pytest.fixture()
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
    address = fake.address()[:255]
    city = fake.city()[:80]
    telephone = fake.phone_number()[:10]

    owner_data = {
        "firstName": firstname,
        "lastName": lastname,
        "address": address,
        "city": city,
        "telephone": telephone
    }
    return owner_data


@pytest.fixture()
def prepare_owner_data_for_update():
    """
    Фикстура для подготовки данных владельца питомца.
    Возвращает json с данными владельца.
    """

    owner_data = {"firstName": "Amber", "lastName": "Franklin", "address": "110", "city": "Madison", "telephone": "6085551023"}
    return json.dumps(owner_data)
