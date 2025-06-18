import json
import allure
import pytest

from helpers import helpers


@pytest.mark.owner
class TestUpdateOwner:
    """

    """

    @allure.title("Обновление инфомрации владельца питомцев")
    def test_update_owner_by_id(self, get_request_instance, create_owner, cleanup_owner, db_client, generate_owner_data):
        owner_id, owner_data = create_owner
        owner_data_for_update = json.dumps(generate_owner_data)
        request = get_request_instance
        request.put(endpoint='api/owners', body=owner_data_for_update, endpoint_id=owner_id)
        new_owner_data = helpers.get_owner_in_db(db_client, owner_id)

        cleanup_owner(owner_id)

        assert helpers.validate_owner_data(owner_id, new_owner_data, json.loads(owner_data_for_update))


    # TODO: Обновить несуществующего, Попытка обновить владельца, у которого есть привязанные питомцы


