##
#
# Copyright (c) 2025, Lorenzo Pouw.
# All rights reserved.
#
##


from .api_client import ClientAPI
from typing import Tuple, Any

class ProPresenterAPI(ClientAPI):
    
    ENDPOINT_VERSION: str = "/version"
    ENDPOINT_TRIGGER: str = "/v1/message/{id}/trigger"
    ENDPOINT_CLEAR: str = "/v1/message/{id}/clear"

    def __init__(self, server_url: str, timeout: int = 5) -> None:
        super().__init__(server_url, timeout)

    def version(self) -> Tuple[bool, Any]:
        success, response = self.get(endpoint=self.ENDPOINT_VERSION, status_codes=[200])
        return success, response if isinstance(response, dict) else None

    def trigger(self, id: str, token: str, message: str) -> Tuple[bool, Any]:
        data = [{"name": token, "text": {"text": message}}]
        return self.post(endpoint=self.ENDPOINT_TRIGGER.format(id=id), data=data, status_codes=[204])

    def clear(self, id: str) -> Tuple[bool, Any]:
        return self.get(endpoint=self.ENDPOINT_CLEAR.format(id=id), status_codes=[204])
