import pytest
import allure

from helpers import helpers


@pytest.mark.smoke
class TestGetPet:
    """

    """

    @allure.title("Получение списка питомцев")
    def test_get_pet_owners(self, get_request_instance, create_owner_with_pets, cleanup_owner):
        pet_id, owner_id, owner_data, data_new_pet = create_owner_with_pets
        request = get_request_instance
        response = request.get(endpoint='api/pets')

        cleanup_owner(owner_id)

        assert helpers.validate_pet_data(pet_id, response, data_new_pet)

    @allure.title("Получение питомца по id")
    def test_get_pet_owner_by_id(self, get_request_instance, create_owner_with_pets, cleanup_owner):
        pet_id, owner_id, owner_data, data_new_pet = create_owner_with_pets
        request = get_request_instance
        response = request.get(endpoint='api/pets', endpoint_id=pet_id)

        cleanup_owner(owner_id)

        assert helpers.validate_pet_data(pet_id, response, data_new_pet)
