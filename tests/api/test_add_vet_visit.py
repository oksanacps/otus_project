import json

import pytest
import allure


@pytest.mark.smoke
@pytest.mark.api
class TestAddVetVisit:
    """ """

    @pytest.mark.nondestructive
    @allure.title("Добавление визита в клинику")
    def test_visit_to_owner_pet(
        self, get_request_instance, create_owner_with_pets, cleanup_owner, db_client
    ):
        pet_id, owner_id, owner_data, data_new_pet = create_owner_with_pets
        request = get_request_instance
        body = {"date": "2013-01-01", "description": "rabies shot"}
        response = request.post(
            endpoint=f"api/owners/{owner_id}/pets/{pet_id}/visits",
            body=json.dumps(body),
            expected_status=201,
        )

        cleanup_owner(owner_id)

        assert response.get("petId") == pet_id
