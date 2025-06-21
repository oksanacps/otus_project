import json
import allure
import pytest

from helpers import helpers


@pytest.mark.smoke
@pytest.mark.api
class TestUpdateOwner:
    """ """

    @pytest.mark.nondestructive
    @allure.title("Обновление инфомрации владельца питомцев без привязанных питомцев")
    def test_update_owner_by_id(
        self,
        get_request_instance,
        create_owner,
        cleanup_owner,
        db_client,
        generate_owner_data,
    ):
        owner_id, owner_data = create_owner
        owner_data_for_update = json.dumps(generate_owner_data)
        request = get_request_instance
        request.put(
            endpoint="api/owners", body=owner_data_for_update, endpoint_id=owner_id
        )
        new_owner_data = helpers.get_owner_in_db(db_client, owner_id)

        cleanup_owner(owner_id)

        assert helpers.validate_owner_data(
            owner_id, new_owner_data, json.loads(owner_data_for_update)
        )

    @pytest.mark.nondestructive
    @allure.title("Обновление инфомрации владельца питомцев с привязанными питомцами")
    def test_update_owner_with_pets(
        self,
        get_request_instance,
        create_owner_with_pets,
        cleanup_owner,
        db_client,
        generate_owner_data,
    ):
        pet_id, owner_id, owner_data, data_new_pet = create_owner_with_pets
        owner_data_for_update = json.dumps(generate_owner_data)
        request = get_request_instance
        request.put(
            endpoint="api/owners", body=owner_data_for_update, endpoint_id=owner_id
        )
        new_owner_data = helpers.get_owner_in_db(db_client, owner_id)

        cleanup_owner(owner_id)

        assert helpers.validate_owner_data(
            owner_id, new_owner_data, json.loads(owner_data_for_update)
        )
