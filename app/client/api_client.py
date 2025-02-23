import logging
import requests
from typing import Any, Tuple, Optional, Dict

class APIClient:
    def __init__(self, server_url: str, headers: Optional[dict] = None) -> None:
        """
        Base class for HTTP requests with error handling.

        Args:
            server_url (str): The base URL of the server.
            headers (dict, optional): Headers for authentication or other purposes.
        """
        self.server_url = server_url
        self.headers = headers or {}
        self._last_result: Optional[Tuple[bool, Any]] = None

    def get(self, endpoint: str, timeout: int = 5, status_codes: Dict = [200]) -> Tuple[bool, Any]:
        """
        Executes a GET request to the specified endpoint.
        
        Args:
            endpoint (str): The endpoint to send the GET request to.
            timeout (int): Timeout in seconds for the request.
            status_codes (Dict): Expected successful status codes.
        
        Returns:
            Tuple[bool, Any]: (True, JSON response) if successful, otherwise (False, None or error message).
        """
        try:
            url = f"{self.server_url}{endpoint}"
            logging.debug(f"Sending GET request to: {url} with headers: {self.headers}")
            response = requests.get(url, headers=self.headers, timeout=timeout)
            if response.status_code in status_codes:
                try:
                    json_data = response.json()
                    return True, json_data
                except ValueError:
                    logging.error("GET request returned non-JSON response.")
                    return False, response.text
            else:
                logging.error(f"GET error: {response.status_code} - {response.text}")
                return False, None
        except requests.exceptions.Timeout:
            logging.error("GET request timed out.")
            return False, None
        except requests.exceptions.RequestException as e:
            logging.error(f"GET request failed: {e}")
            return False, None

    def post(self, endpoint: str, data: Dict[str, Any], timeout: int = 5, status_codes: Dict = [200]) -> Tuple[bool, Any]:
        """
        Executes a POST request to the specified endpoint.
        
        Args:
            endpoint (str): The endpoint to send the POST request to.
            data (Dict[str, Any]): The data to send in the POST request.
            timeout (int): Timeout in seconds for the request.
            status_codes (Dict): Expected successful status codes.
        
        Returns:
            Tuple[bool, Any]: (True, JSON response) if successful, otherwise (False, None or error message).
        """
        try:
            url = f"{self.server_url}{endpoint}"
            logging.debug(f"Sending POST request to: {url} with headers: {self.headers} and data: {data}")
            response = requests.post(url, json=data, headers=self.headers, timeout=timeout)
            if response.status_code in status_codes:
                try:
                    json_data = response.json()
                    return True, json_data
                except ValueError:
                    logging.error("POST request returned non-JSON response.")
                    return False, response.text
            else:
                logging.error(f"POST error: {response.status_code} - {response.text}")
                return False, None
        except requests.exceptions.Timeout:
            logging.error("POST request timed out.")
            return False, None
        except requests.exceptions.RequestException as e:
            logging.error(f"POST request failed: {e}")
            return False, None

    def delete(self, endpoint: str, timeout: int = 5, status_codes: Dict = [200, 204]) -> Tuple[bool, Any]:
        """
        Executes a DELETE request to the specified endpoint.
        
        Args:
            endpoint (str): The endpoint to send the DELETE request to.
            timeout (int): Timeout in seconds for the request.
            status_codes (Dict): Expected successful status codes.
        
        Returns:
            Tuple[bool, Any]: (True, None) if successful, otherwise (False, None).
        """
        try:
            url = f"{self.server_url}{endpoint}"
            logging.debug(f"Sending DELETE request to: {url} with headers: {self.headers}")
            response = requests.delete(url, headers=self.headers, timeout=timeout)
            if response.status_code in status_codes:
                return True, None  # No body needed for a successful deletion
            else:
                logging.error(f"DELETE error: {response.status_code} - {response.text}")
                return False, None
        except requests.exceptions.Timeout:
            logging.error("DELETE request timed out.")
            return False, None
        except requests.exceptions.RequestException as e:
            logging.error(f"DELETE request failed: {e}")
            return False, None
