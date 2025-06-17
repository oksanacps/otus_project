from src.database.my_sql.db_client import MySqlDbClient


def create_owner(db_client: MySqlDbClient, customer_data: dict):
    """
    Создает владельца в БД.
    Возвращает id созданного клиента.
    """

    params = (
        customer_data.get("firstName"),
        customer_data.get("lastName"),
        customer_data.get("address"),
        customer_data.get("city"),
        customer_data.get("telephone"),
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
        sql_select = "SELECT LAST_INSERT_ID();"
        result = db_client.execute(sql_select)
        return result[0][0]

    except Exception:
        raise AssertionError(f"Ошибка создания владельца")
    

def delete_owner(db_client: MySqlDbClient, id: int):
    """
    Удаляет владельца питомца по ID.
    Возвращает True (БД кол-во затронутых строк не возвращает??)
    """
    params = (
        id
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
        raise ArithmeticError(f"Ошибка удаления владельца{id}: {e}")