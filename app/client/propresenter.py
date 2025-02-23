from .api_client import APIClient
from typing import Tuple, Any

class ProPresenter(APIClient):
    def __init__(self, server_url: str, timeout: int = 5) -> None:
        """
        ProPresenter class for executing REST API requests with authentication.
        
        Args:
            server_url (str): The base URL of the REST API Executor server.
            timeout (int): Timeout in seconds for the request.
        """
        super().__init__(server_url= server_url, timeout=timeout)

    def version(self) -> Tuple[bool, Any]:
        """
        Checks if the ProPresenter server is online by querying the /version endpoint.
        
        See: https://openapi.propresenter.com/#/Status/versionGet for more information.

        Returns:
            Tuple[bool, Any]: (True, JSON response) if the server is online, otherwise (False, None).
        """
        return self.get(endpoint="/version", status_codes=[200])
    
    def trigger(self, id: str, token: str, message: str) -> Tuple[bool, Any]:
        """
        Sends a trigger request with the provided token and message.
        
        See: https://openapi.propresenter.com/#/Message/messageTrigger for more information.

        Args:
            id (str): ID of the message to be triggered.
            token (str): Auth token or name required for authentication.
            message (str): The message content to be sent.

        Returns:
            Tuple[bool, Any]: A tuple containing a success boolean and response data.
        """
        data = [{"name": token, "text": {"text": message}}]
        return self.post(endpoint=f"/v1/message/{id}/trigger", data=data, status_codes=[204])

    def clear(self, id: str) -> Tuple[bool, Any]:
        """
        Sends a clear request to delete a message with the specified ID.
        
        See: https://openapi.propresenter.com/#/Message/messageClear for more information.

        Args:
            id (str): The ID of the message to be cleared.

        Returns:
            Tuple[bool, Any]: A tuple with a success boolean and response data (None if status code is 204).
        """
        return self.get(endpoint=f"/v1/message/{id}/clear", status_codes=[204])

    def layer_status(self) -> Tuple[bool, Any]:
        """
        Retrieves the status of the layers from the ProPresenter server.
        
        See: https://openapi.propresenter.com/#/Status/layerStatusGet for more information.

        Returns:
            Tuple[bool, Any]: A tuple containing a success boolean and the layer status response.
        """
        return self.get(endpoint="/v1/status/layers", status_codes=[200])
