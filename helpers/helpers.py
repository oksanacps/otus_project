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
        owner_in_response = next(
            (owner for owner in response if owner['id'] == owner_id),
            None
        )

        if not owner_in_response:
            return False
    else:
        owner_in_response = response

    for field in ['firstName', 'lastName', 'address', 'city', 'telephone']:
        if owner_in_response.get(field) != expected_data.get(field):
            return False

    return True


def get_owner_in_db(db_client, owner_id):
    result = db_steps.get_owner_by_id(db_client, owner_id)
    if result:
        return {
            "firstName": result[0]['first_name'],
            "lastName": result[0]['last_name'],
            "address": result[0]['address'],
            "city": result[0]['city'],
            "telephone": result[0]['telephone']
        }
    return None
