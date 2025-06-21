import pytest
import allure

from helpers import helpers


@pytest.mark.smoke
@pytest.mark.api
class TestDeleteOwner:
    """ """

    @pytest.mark.nondestructive
    @allure.title("Удаление владельца питомцев по id без привязанных питомцев")
    def test_delete_owner_by_id(
        self, get_request_instance, create_owner, cleanup_owner, db_client
    ):
        owner_id, owner_data = create_owner
        request = get_request_instance
        request.delete(endpoint="api/owners", endpoint_id=owner_id)

        cleanup_owner(owner_id)

        assert helpers.get_owner_in_db(db_client, owner_id) is None

    @pytest.mark.nondestructive
    @allure.title("Удаление владельца с привязанными питомцами")
    def test_delete_owner_with_pets(
        self, get_request_instance, create_owner_with_pets, cleanup_owner, db_client
    ):
        pet_id, owner_id, owner_data, data_new_pet = create_owner_with_pets
        request = get_request_instance
        response = request.delete(
            endpoint="api/owners", endpoint_id=owner_id, expected_status=404
        )

        cleanup_owner(owner_id)

        assert "Cannot delete or update a parent row" in response["detail"]
