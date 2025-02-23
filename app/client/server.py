from .api_client import APIClient
from typing import Tuple, Any

class Server(APIClient):
    def __init__(self, server_url: str, api_key: str, timeout: int = 5) -> None:
        """
        Server class for executing REST API requests with authentication.
        
        Args:
            server_url (str): The base URL of the REST API Executor server.
            timeout (int): Timeout in seconds for the request.
            api_key (str): API key used for authentication.
        """
        super().__init__(server_url= server_url, headers={'X-API-Key': api_key}, timeout=timeout)

    def get_status(self) -> Tuple[bool, Any]:
        """
        Checks if the REST API Executor server is online by sending a GET request.

        Returns:
            Tuple[bool, Any]: (True, JSON response) if the server is online, otherwise (False, None).
        """
        return self.get(endpoint="/api/v1")
    
    def get_commands(self) -> Tuple[bool, Any]:
        """
        Get an list of all available commands.

        Returns:
            Tuple[bool, Any]: (True, JSON response) if the server is online, otherwise (False, None).
        """     
        return self.get(endpoint='/api/v1/commands')
    
    def clear_commands(self) -> Tuple[bool, Any]:    
        """
        Clear the commands buffer,

        Returns:
            Tuple[bool, Any]: (True, JSON response) if the server is online, otherwise (False, None).
        """
        return self.delete(endpoint="/api/v1/commands") 