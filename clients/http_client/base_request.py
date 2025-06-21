import requests
from logger import logger_events


class BaseRequest:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers

    def _request(self, url, request_type, data=None, params=None):
        if request_type == "GET":
            response = requests.get(url, params=params, headers=self.headers, timeout=5)
        elif request_type == "POST":
            response = requests.post(url, data=data, headers=self.headers, timeout=5)
        elif request_type == "DELETE":
            response = requests.delete(url, headers=self.headers, timeout=5)
        elif request_type == "PUT":
            response = requests.put(url, data=data, headers=self.headers, timeout=5)
        else:
            raise ValueError(f"Unsupported request type: {request_type}")

        return response

    def _build_url(self, endpoint=None, endpoint_id=None):
        url = self.base_url
        if endpoint:
            url += f"/{endpoint}"
        if endpoint_id:
            url += f"/{endpoint_id}"
        return url

    def _process_response(self, response, expected_status=200):
        logger_events.http_event_log(response=response)
        assert response.status_code == expected_status
        try:
            return response.json()
        except ValueError:
            return response

    def get(self, endpoint=None, endpoint_id=None, params=None, expected_status=200):
        url = self._build_url(endpoint, endpoint_id)
        response = self._request(url=url, request_type="GET", params=params)
        return self._process_response(response, expected_status)

    def post(self, endpoint, body, endpoint_id=None, expected_status=200):
        url = self._build_url(endpoint, endpoint_id)
        response = self._request(url, "POST", data=body)
        return self._process_response(response, expected_status)

    def delete(self, endpoint, endpoint_id=None, expected_status=204):
        url = self._build_url(endpoint, endpoint_id)
        response = self._request(url, "DELETE")
        return self._process_response(response, expected_status)

    def put(self, endpoint, body, endpoint_id=None, expected_status=204):
        url = self._build_url(endpoint, endpoint_id)
        response = self._request(url, "PUT", data=body)
        return self._process_response(response, expected_status)
