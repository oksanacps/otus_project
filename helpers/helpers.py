from db_steps import db_steps


def validate_owner_data(owner_id, response, expected_data):
    """
    Проверяет, что данные владельца в ответе соответствуют ожидаемым

    :param owner_id: ID владельца для проверки
    :param response: Ответ API (список владельцев)
    :param expected_data: Ожидаемые данные владельца
    :return: True если данные соответствуют, False если нет
    """

    if type(response) is list:
        owner_in_response = find_by_id(response, owner_id)

        if not owner_in_response:
            return False
    else:
        owner_in_response = response

    for field in ["firstName", "lastName", "address", "city", "telephone"]:
        if owner_in_response.get(field) != expected_data.get(field):
            return False

    return True


def validate_pet_data(pet_id, response, expected_data):
    """
    Проверяет, что данные владельца в ответе соответствуют ожидаемым

    :param pet_id: ID питомца для проверки
    :param response: Ответ API (список питомцев)
    :param expected_data: Ожидаемые данные питомца
    :return: True если данные соответствуют, False если нет
    """

    if isinstance(response, list):
        pet_in_response = find_by_id(response, pet_id)

        if not pet_in_response:
            return False
    else:
        pet_in_response = response

    for field in ["name", "birthDate", "type"]:
        if pet_in_response.get(field) != expected_data.get(field):
            return False

    return True


def get_owner_in_db(db_client, owner_id):
    result = db_steps.get_owner_by_id(db_client, owner_id)
    if result:
        return {
            "firstName": result[0]["first_name"],
            "lastName": result[0]["last_name"],
            "address": result[0]["address"],
            "city": result[0]["city"],
            "telephone": result[0]["telephone"],
        }
    return None


def get_pet_in_db(db_client, pet_id):
    result = db_steps.get_pet_by_id(db_client, pet_id)
    if result:
        return result[0]
    return None


def find_by_id(items, item_id):
    return next((item for item in items if item["id"] == item_id), None)
