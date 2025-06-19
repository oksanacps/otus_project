import pymysql
import pymysql.cursors
from logger.logger_events import db_event_log


class MySqlDbClient:
    def __init__(self, host: str, port: int, user: str, password: str, db: str):
        self.connection = pymysql.connect(
            host=host, port=port, user=user, db=db, password=password
        )

    def execute(self, sql_request: str, params: tuple = None):
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql_request, params)
                self.connection.commit()
                raw_data = cursor.fetchall()
                db_event_log(host_info=self.connection.get_host_info(), sql_request=sql_request, params=params, raw_data=raw_data)

            return raw_data

        except Exception as e:
            self.connection.rollback()
            db_event_log(host_info=self.connection.get_host_info(), sql_request=sql_request, params=params,
                         raw_data=str(raw_data))

            raise AssertionError(f"Ошибка выполнения SQL запроса: {e}")

    def close(self):
        self.connection.close()
