from .api_client import APIClient
from typing import Tuple, Any

class Server(APIClient):
    def __init__(self, server_url: str, api_key: str) -> None:
        """
        Server class for executing REST API requests with authentication.
        
        Args:
            server_url (str): The base URL of the REST API Executor server.
            api_key (str): API key used for authentication.
        """
        super().__init__(server_url, headers={'X-API-Key': api_key})

    def get_status(self) -> Tuple[bool, Any]:
        """
        Checks if the REST API Executor server is online by sending a GET request.

        Returns:
            Tuple[bool, Any]: (True, JSON response) if the server is online, otherwise (False, None).
        """
        return self.get("/api/v1")
