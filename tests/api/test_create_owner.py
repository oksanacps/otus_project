import json

import pytest
import allure

from helpers import helpers


@pytest.mark.api
class TestCreateOwner:
    """ """

    @pytest.mark.nondestructive
    @allure.title("Создание владельца питомцев")
    @pytest.mark.smoke
    def test_create_owner(
        self, get_request_instance, cleanup_owner, db_client, generate_owner_data
    ):
        request = get_request_instance
        data_new_owner = json.dumps(generate_owner_data)
        response = request.post(
            endpoint="api/owners", body=data_new_owner, expected_status=201
        )
        owner_id = response.get("id")

        cleanup_owner(owner_id)

        assert helpers.validate_owner_data(owner_id, response, generate_owner_data)

    @pytest.mark.nondestructive
    @allure.title("Создание владельца без обязательных параметров в теле запроса")
    @pytest.mark.regress
    @pytest.mark.parametrize(
        "field, expected_status",
        [("firstName", 400), ("lastName", 400), ("telephone", 400)],
    )
    def test_create_owner_missing_required_field(
        self,
        get_request_instance,
        generate_owner_data,
        field,
        expected_status,
        cleanup_owner,
    ):
        request = get_request_instance
        data_new_owner = generate_owner_data
        del data_new_owner[field]
        response = request.post(
            "api/owners",
            body=json.dumps(data_new_owner),
            expected_status=expected_status,
        )
        assert (
            f"Field error in object 'ownerFieldsDto' on field '{field}'"
            in response["detail"]
        )

    @pytest.mark.nondestructive
    @allure.title(
        "Проверка ошибки при превышении максимальной длины полей в запросе создания владельца"
    )
    @pytest.mark.regress
    @pytest.mark.parametrize(
        "field, value, expected_status",
        [
            ("firstName", "A" * 31, 400),
            ("lastName", "A" * 31, 400),
            ("address", "A" * 256, 400),
            ("city", "A" * 81, 400),
            (
                "telephone",
                "12345678901",
                400,
            ),  # Специально, что бы в отчете были падения
        ],
    )
    def test_create_owner_field_length_validation(
        self,
        get_request_instance,
        generate_owner_data,
        field,
        value,
        expected_status,
        cleanup_owner,
    ):
        data_new_owner = generate_owner_data
        data_new_owner[field] = value
        response = get_request_instance.post(
            "api/owners",
            body=json.dumps(data_new_owner),
            expected_status=expected_status,
        )
        assert (
            f"Field error in object 'ownerFieldsDto' on field '{field}'"
            in response["detail"]
        )
