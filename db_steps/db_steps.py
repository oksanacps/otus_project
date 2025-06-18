from src.database.my_sql.db_client import MySqlDbClient


def create_owner(db_client: MySqlDbClient, owner_data: dict):
    """
    Создает владельца в БД.
    Возвращает id созданного владельца.
    """

    params = (
        owner_data.get("firstName"),
        owner_data.get("lastName"),
        owner_data.get("address"),
        owner_data.get("city"),
        owner_data.get("telephone"),
    )

    sql_request = """
        INSERT INTO owners
            (first_name, last_name, 
            address, 
            city, 
            telephone)
        VALUES (%s, %s, %s, %s, %s);
    """

    try:
        db_client.execute(sql_request, params)
        sql_select = "SELECT LAST_INSERT_ID() as id;"
        result = db_client.execute(sql_select)
        return result[0].get('id')

    except Exception:
        raise AssertionError(f"Ошибка создания владельца")
    

def delete_owner(db_client: MySqlDbClient, owner_id: int):
    """
    Удаляет владельца питомца по ID.
    Возвращает True (БД кол-во затронутых строк не возвращает??)
    """
    params = (
        owner_id,
    )

    sql_request = """
        DELETE
        FROM owners
        WHERE id = %s;
        """

    try:
        db_client.execute(sql_request, params)
        return True

    except Exception as e:
        raise ArithmeticError(f"Ошибка удаления владельца {owner_id}: {e}")


def get_owner_by_id(db_client: MySqlDbClient, owner_id: int):
    """
    Получает владельца питомца по ID.
    """
    params = (
        owner_id,
    )

    sql_request = """
        SELECT *
        FROM owners
        WHERE id = %s;
        """

    try:
        result = db_client.execute(sql_request, params)
        return result

    except Exception as e:
        raise ArithmeticError(f"Ошибка получения владельца {owner_id}: {e}")


def get_pet_by_id(db_client: MySqlDbClient, pet_id: int):
    """
    Получает питомца по ID.
    """
    params = (
        pet_id,
    )

    sql_request = """
        SELECT *
        FROM pets
        WHERE id = %s;
        """

    try:
        result = db_client.execute(sql_request, params)
        return result

    except Exception as e:
        raise ArithmeticError(f"Ошибка получения питомца {pet_id}: {e}")


def get_all_pets_by_owner_id(db_client: MySqlDbClient, owner_id: int):
    """
    Получает всех питомцев по ID владельца.
    """
    params = (
        owner_id,
    )

    sql_request = """
        SELECT *
        FROM pets
        WHERE owner_id = %s;
        """

    try:
        result = db_client.execute(sql_request, params)
        return result

    except Exception as e:
        raise ArithmeticError(f"Ошибка получения питомцев по владельцу {owner_id}: {e}")


def delete_all_pets_by_owner_id(db_client: MySqlDbClient, owner_id: int):
    """
    Удаляет всех питомцев по ID владельца.
    """
    params = (
        owner_id,
    )

    sql_request = """
        DELETE
        FROM pets
        WHERE owner_id = %s;
        """

    try:
        db_client.execute(sql_request, params)
        return True

    except Exception as e:
        raise ArithmeticError(f"Ошибка получения питомца {owner_id}: {e}")


def delete_all_visits_by_pet_id(db_client: MySqlDbClient, pet_id: int):
    """
    Удаляет все виситы в клиенику по ID питомца.
    """
    params = (
        pet_id,
    )

    sql_request = """
        DELETE
        FROM visits
        WHERE pet_id = %s;
        """

    try:
        db_client.execute(sql_request, params)
        return True

    except Exception as e:
        raise ArithmeticError(f"Ошибка получения визита {pet_id}: {e}")


def get_pet_types(db_client: MySqlDbClient):
    """
    Получает типы питомцев.
    """

    sql_request = """
        SELECT *
        FROM types;
        """

    try:
        result = db_client.execute(sql_request)
        return result

    except Exception as e:
        raise ArithmeticError(f"Ошибка получения типов питомцев: {e}")
