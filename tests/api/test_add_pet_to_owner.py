import json

import pytest
import allure

from helpers import helpers


@pytest.mark.owner
class TestAddPetToOwner:
    """

    """

    @pytest.mark.test
    @allure.title("Добавление питомца владельцу")
    def test_add_pet_to_owner(self, get_request_instance, create_owner, cleanup_owner, db_client, generate_pet_data):
        owner_id, owner_data = create_owner
        request = get_request_instance
        data_new_pet = generate_pet_data
        response = request.post(endpoint=f'api/owners/{owner_id}/pets', body=json.dumps(data_new_pet))
        pet_id = response.get('id')
        pet_data = helpers.get_pet_in_db(db_client, pet_id)

        cleanup_owner(owner_id)

        assert pet_data.get('owner_id') == owner_id

