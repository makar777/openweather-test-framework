import urllib.request
from urllib.error import HTTPError


class HttpUtils:

    @staticmethod
    def query_service(url=None):
        try:
            with urllib.request.urlopen(f"{url}") as response:
                response_status = response.status
                response_data = response.read()
                return response_data, response_status
        except HTTPError as e:
            return None, e.code
