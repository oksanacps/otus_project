import pytest
import allure
import jsonschema

from helpers import helpers, schems


@pytest.mark.smoke
@pytest.mark.api
class TestGetOwner:
    """ """

    @pytest.mark.nondestructive
    @allure.title("Получение списка владельцев питомцев")
    def test_get_pet_owners(self, get_request_instance, create_owner, cleanup_owner):
        owner_id, owner_data = create_owner
        request = get_request_instance
        response = request.get(endpoint="api/owners")

        cleanup_owner(owner_id)

        assert helpers.validate_owner_data(owner_id, response, owner_data)
        jsonschema.validate(instance=response, schema=schems.schema_get_owners)

    @pytest.mark.nondestructive
    @allure.title("Получение владельца питомцев по id")
    def test_get_pet_owner_by_id(
        self, get_request_instance, create_owner, cleanup_owner
    ):
        owner_id, owner_data = create_owner
        request = get_request_instance
        response = request.get(endpoint="api/owners", endpoint_id=owner_id)

        cleanup_owner(owner_id)

        assert helpers.validate_owner_data(owner_id, response, owner_data)
