import pytest
import allure

from helpers import helpers


@pytest.mark.smoke
@pytest.mark.api
class TestDeletePet:
    """ """

    @pytest.mark.nondestructive
    @allure.title("Удаление питомца по id без привязанных визитов")
    def test_delete_pet_by_id(
        self, get_request_instance, create_owner_with_pets, cleanup_owner, db_client
    ):
        pet_id, owner_id, owner_data, data_new_pet = create_owner_with_pets
        request = get_request_instance
        response = request.delete(endpoint="api/pets", endpoint_id=pet_id)

        cleanup_owner(owner_id)

        assert helpers.get_pet_in_db(db_client, owner_id) is None

    @pytest.mark.nondestructive
    @allure.title("Удаление питомцев с привязанными визитами")
    def test_delete_pet_with_visits(
        self,
        get_request_instance,
        create_owner_with_pets_visit,
        cleanup_owner,
        db_client,
    ):
        pet_id, owner_id, owner_data, data_new_pet, visit_data = (
            create_owner_with_pets_visit
        )
        request = get_request_instance
        response = request.delete(
            endpoint="api/pets", endpoint_id=pet_id, expected_status=404
        )

        cleanup_owner(owner_id)

        assert "Cannot delete or update a parent row" in response["detail"]
