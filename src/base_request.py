import requests


class BaseRequest:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers

    def _request(self, url, request_type, data=None, params=None):
        if request_type == 'GET':
            response = requests.get(url, params=params)
        elif request_type == 'POST':
            response = requests.post(url, data=data)
        elif request_type == 'DELETE':
            response = requests.delete(url)
        elif request_type == 'PUT':
            response = requests.put(url, data=data)
        else:
            response = requests.delete(url)

        # log part
        print('*************')
        print(f'{request_type}')
        print(response.url)
        print(response.status_code)
        print(response.reason)
        print(response.text)
        print(response.json())
        print('*************')
        return response

    def get(self, endpoint=None, endpoint_id=None, params=None):
        if endpoint is not None and endpoint_id is None:
            url = f'{self.base_url}/{endpoint}'
        elif endpoint is None and endpoint_id is None:
            url = self.base_url
        elif endpoint is not None and endpoint_id is not None:
            url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url=url, request_type='GET', params=params)
        assert response.status_code == 200
        return response.json()

    def post(self, endpoint, body, endpoint_id=None):
        if endpoint_id is None:
            url = f'{self.base_url}/{endpoint}'
        else:
            url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'POST', data=body)
        assert response.status_code == 200
        return response.json()

    def delete(self, endpoint, endpoint_id=None):
        if endpoint_id is None:
            url = f'{self.base_url}/{endpoint}'
        else:
            url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        assert response.status_code == 200
        return response.json()

    def put(self, endpoint, body, endpoint_id=None):
        if endpoint_id is None:
            url = f'{self.base_url}/{endpoint}'
        else:
            url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'PUT', data=body)
        assert response.status_code == 200
        return response.json()
