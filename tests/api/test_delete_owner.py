import pytest
import allure

from helpers import helpers


@pytest.mark.owner
class TestDeleteOwner:
    """

    """

    @allure.title("Удаление владельца питомцев по id")
    def test_delete_owner_by_id(self, get_request_instance, create_owner, cleanup_owner, db_client):
        owner_id, owner_data = create_owner
        request = get_request_instance
        response = request.delete(endpoint='api/owners', endpoint_id=owner_id)

        cleanup_owner(owner_id)

        assert response.status_code == 204
        assert helpers.get_owner_in_db(db_client, owner_id) is None

