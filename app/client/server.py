from .api_client import APIClient
from typing import Tuple, Any

class Server(APIClient):
    def __init__(self, server_url: str, api_key: str, timeout: int = 5) -> None:
        """
        Initializes the Server class to interact with the REST API Executor, providing authentication and request configuration.
        
        Args:
            server_url (str): The base URL for the REST API Executor.
            api_key (str): The API key used for authenticating requests.
            timeout (int): The number of seconds before a request times out (default is 5 seconds).
        """
        super().__init__(server_url= server_url, headers={'X-API-Key': api_key}, timeout=timeout)

    def version(self) -> Tuple[bool, Any]:
        """
        Verifies the server's availability by sending a GET request to check its status.

        Returns:
            Tuple[bool, Any]: A tuple where the first value is True if the request was successful (along with the JSON response), 
                               or False if the request failed (with None as the second value).
        """
        return self.get(endpoint="/api/v1")
    
    def get_commands(self) -> Tuple[bool, Any]:
        """
        Retrieves a list of all available commands from the server.

        Returns:
            Tuple[bool, Any]: A tuple where the first value is True if the server is reachable and returns the JSON response, 
                               or False if the request fails (with None as the second value).
        """
        return self.get(endpoint='/api/v1/commands')
    
    def clear_commands(self) -> Tuple[bool, Any]:    
        """
        Clears the current commands stored on the server.

        Returns:
            Tuple[bool, Any]: A tuple where the first value is True if the server successfully processed the request, 
                               or False if the request fails (with None as the second value).
        """
        return self.delete(endpoint="/api/v1/commands")

    def clear_command(self, uuid:str) -> Tuple[bool, Any]:    
        """
        Clears an specific command stored on the server.
        
        Args:
            uuid (str): The unique user id of the command.
            
        Returns:
            Tuple[bool, Any]: A tuple where the first value is True if the server successfully processed the request, 
                               or False if the request fails (with None as the second value).
        """
        data = [{"uuid": uuid}]
        return self.delete(endpoint="/api/v1/command", data=data)
