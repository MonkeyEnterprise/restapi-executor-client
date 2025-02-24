import logging
import requests
from typing import Any, Tuple, Optional, List, Dict

class APIClient:
    def __init__(self, server_url: str, headers: Optional[dict] = None, timeout: int = 5) -> None:
        """
        Base class for HTTP requests with error handling.

        Args:
            server_url (str): The base URL of the server.
            timeout (int): Timeout in seconds for the requests.
            headers (dict, optional): Headers for authentication or other purposes.
        """
        self.server_url = server_url
        self.headers = headers or {}
        self.timeout = timeout
        self._last_result: Optional[Tuple[bool, Any]] = None

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                      status_codes: List[int] = [200]) -> Tuple[bool, Any]:
        """
        Helper method to make HTTP requests (GET, POST, DELETE).

        Args:
            method (str): HTTP method ('GET', 'POST', or 'DELETE').
            endpoint (str): The endpoint to send the request to.
            data (Optional[Dict[str, Any]]): Data to be sent in the request (for POST).
            status_codes (List[int]): Expected successful status codes.

        Returns:
            Tuple[bool, Any]: (True, response data) if successful, otherwise (False, error message).
        """
        try:
            url = f"{self.server_url}{endpoint}"
            request_data = {'headers': self.headers, 'timeout': self.timeout}
            
            if method == 'POST':
                request_data['json'] = data
                logging.debug(f"Sending POST request to: {url} with data: {data}")
                response = requests.post(url, **request_data)
            elif method == 'DELETE':
                logging.debug(f"Sending DELETE request to: {url}")
                response = requests.delete(url, **request_data)
            else:  # Default to GET
                logging.debug(f"Sending GET request to: {url}")
                response = requests.get(url, **request_data)
            
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
        """Executes a GET request."""
        return self._make_request('GET', endpoint, status_codes=status_codes)

    def post(self, endpoint: str, data: Dict[str, Any], status_codes: List[int] = [200]) -> Tuple[bool, Any]:
        """Executes a POST request."""
        return self._make_request('POST', endpoint, data=data, status_codes=status_codes)

    def delete(self, endpoint: str, status_codes: List[int] = [200, 204]) -> Tuple[bool, Any]:
        """Executes a DELETE request."""
        return self._make_request('DELETE', endpoint, status_codes=status_codes)
