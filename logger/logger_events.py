import json
import uuid
import inspect

import requests
from requests import JSONDecodeError

import allure
from allure_commons.types import AttachmentType


from logger import custom_logger


def db_event_log(host_info, sql_request, params, raw_data):

    with allure.step('Отправить запрос в БД'):
        allure.attach(body=host_info, name='Host', attachment_type=AttachmentType.TEXT)
        allure.attach(body=sql_request, name='SQL запрос', attachment_type=AttachmentType.TEXT)
        params_str = str(params) if params is not None else "None"
        allure.attach(body=params_str, name='Параметры запроса', attachment_type=AttachmentType.TEXT)
        raw_data_str = str(raw_data) if not isinstance(raw_data, str) else raw_data
        allure.attach(body=raw_data_str, name='Результат запроса',
                      attachment_type=allure.attachment_type.JSON if isinstance(raw_data, (dict, list))
                      else allure.attachment_type.TEXT)

    msg = f"======================== Начало логирование события выполнения запроса в БД ========================\n" \
          f"- HOST: {host_info}\n" \
          f"- SQL запрос: {sql_request}\n" \
          f"- Параметры запрос: {params}\n" \
          f"- Результат выполнения запроса: {raw_data}" \

    footer_msg = "======================== Конец логирования события выполнения запроса в БД ========================\n"
    custom_logger.logger.info(msg)
    custom_logger.logger.info(footer_msg)


def convert_request_to_curl(request: requests.PreparedRequest):
    """Конвертировать объект запроса requests.PreparedRequest в эквивалентную команду curl.

    Args:
        request: объект requests.PreparedRequest для преобразования.

    Returns:
        curl_string: str curl.
    """
    method = request.method
    uri = request.url
    data = request.body
    headers = ['"{0}: {1}"'.format(k, v) for k, v in request.headers.items()]
    headers = " -H ".join(headers)

    curl_string = f"curl -X {method} -H {headers} -d '{data}' '{uri}'"

    return curl_string


def http_event_log(response: requests.Response, event_id=None):
    """Вывести информацию о событиях связанных с HTTP-запросами и ответами в консоль.
    Этот метод создает уникальный идентификатор события при выводе.

    Args:
        response: ответ от HTTP-сервера в формате requests.Response.
        event_id: уникальный идентификатор события для вывода в консоль. Если None - сгенерировать случайный.
    """
    if event_id is None:
        event_id = str(uuid.uuid4())

    curl = convert_request_to_curl(request=response.request)
    body_msg = []

    head_msg = "========================= Вывод информации о событии HTTP запроса/ответа ========================="
    footer_msg = "===================== Конец вывода информации о событии HTTP запроса/ответа ====================="

    body_msg.append(head_msg)
    body_msg.append(f'- URL: {response.request.url}')
    body_msg.append(f'- Method: {response.request.method}')
    body_msg.append(f'- Request headers: {response.request.headers}')
    body_msg.append(f'- Request CURL: {curl}')
    body_msg.append(f'- Request status_code: {response.status_code}')

    try:
        json_response = response.json()
        body_msg.append(f'- Response JSON: {json.dumps(json_response, indent=2)}')
    except JSONDecodeError:
        body_msg.append(f'- Response Body: {response.text}')

    info_msg = '\n'.join(body_msg)

    custom_logger.logger.newline()
    custom_logger.logger.info(info_msg, extra={'event_id': event_id})
    custom_logger.logger.info(footer_msg, extra={'event_id': event_id})


def log_ui_event(*args, event_id=None):
    """Вывести информацию о событиях связанных с поиском элемента.
    Этот метод создает уникальный идентификатор события при выводе.

    Args:
        *args: url переданный на откртытие или локатор
        action: логируемое действие
        event_id: уникальный идентификатор события для вывода в консоль. Если None - сгенерировать случайный.
    """
    caller_frame = inspect.currentframe().f_back
    action = caller_frame.f_code.co_name

    if event_id is None:
        event_id = str(uuid.uuid4())

    body_msg = []

    head_msg = "========================= Вывод информации о UI событии ========================="
    footer_msg = "===================== Конец вывода информации о UI событии ====================="

    body_msg.append(head_msg)
    if args and isinstance(args[0], str):
        body_msg.append(f'- URL: {args[0]}')
    elif args and isinstance(args[0], tuple):
        body_msg.append(f'- Locator: {args[0][0]}')
        body_msg.append(f'- Selector: {args[0][1]}')
    body_msg.append(f'- Action: {action}')

    info_msg = '\n'.join(body_msg)

    custom_logger.logger.newline()
    custom_logger.logger.info(info_msg, extra={'event_id': event_id})
    custom_logger.logger.info(footer_msg, extra={'event_id': event_id})
