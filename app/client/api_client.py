##
#
# Copyright (c) 2025, Lorenzo Pouw.
# All rights reserved.
#
##


import logging
import requests
from typing import Any, Tuple, Optional, List, Dict

class ClientAPI:
    def __init__(self, server_url: str, headers: Optional[dict] = None, timeout: int = 5) -> None:
        self.server_url = server_url
        self.headers = headers if isinstance(headers, dict) else {}
        self.timeout = timeout

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                      status_codes: List[int] = [200]) -> Tuple[bool, Any]:
        try:
            url = f"{self.server_url}{endpoint}"
            request_data = {'headers': self.headers, 'timeout': self.timeout, 'json': data}

            match method.upper():
                case "GET":
                    logging.debug(f"Sending GET request to: {url}")
                    response = requests.get(url, headers=self.headers, timeout=self.timeout)

                case "POST":
                    logging.debug(f"Sending POST request to: {url} with data: {data}")
                    response = requests.post(url, **request_data)

                case "DELETE":
                    logging.debug(f"Sending DELETE request to: {url} with data: {data}")
                    response = requests.delete(url, **request_data)

                case _:
                    logging.error(f"Unsupported HTTP method: {method}")
                    return False, None

            if response.status_code in status_codes:
                try:
                    return True, response.json()
                except ValueError:
                    logging.error(f"{method} request returned non-JSON response.")
                    return False, response.text
            else:
                logging.error(f"{method} request failed with status {response.status_code}: {response.text}")
                return False, None

        except requests.exceptions.Timeout:
            logging.error(f"{method} request timed out.")
            return False, None
        except requests.exceptions.RequestException as e:
            logging.error(f"{method} request failed: {e}")
            return False, None

    def get(self, endpoint: str, status_codes: List[int] = [200]) -> Tuple[bool, Any]:
        return self._make_request('GET', endpoint, status_codes=status_codes)

    def post(self, endpoint: str, data: Dict[str, Any], status_codes: List[int] = [200]) -> Tuple[bool, Any]:
        return self._make_request('POST', endpoint, data=data, status_codes=status_codes)

    def delete(self, endpoint: str, data: Optional[Dict[str, Any]] = None, status_codes: List[int] = [200, 204]) -> Tuple[bool, Any]:
        return self._make_request('DELETE', endpoint, data=data, status_codes=status_codes)
