import pymysql
import logging
import pymysql.cursors


class MySqlDbClient:
    def __init__(self, host: str, port: int, user: str, password: str, db: str):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            db=db,
            password=password
        )

    def execute(self, sql_request: str, params: tuple = None):
        try:
            with self.connection.cursor() as cursor: 
                cursor.execute(sql_request, params)
                self.connection.commit()
                raw_data = cursor.fetchall()
                logging.info(f"--------------------------------")
                logging.info(self.connection.get_host_info())
            logging.info(f"Executed SQL request: {sql_request}")
            logging.info(f"Parameters: {params}")
            logging.info(f"Raw data: {raw_data}")
            logging.info(f"--------------------------------")
            return raw_data
        except Exception as e:
            logging.error(f"Error executing SQL request: {e}")
            self.connection.rollback()
            raise AssertionError(f"Ошибка выполнения SQL запроса: {e}")

    def close(self):
        logging.info("Closing DB connection...")
        self.connection.close()