##
#
# Copyright (c) 2025, Lorenzo Pouw.
# All rights reserved.
#
##


from .api_client import ClientAPI
from typing import Tuple, Any

class ExecutorAPI(ClientAPI):

    ENDPOINT_VERSION: str = "/api/v1"
    ENDPOINT_GET_COMMANDS: str = "/api/v1/commands"
    ENDPOINT_CLEAR_COMMANDS: str = "/api/v1/commands"
    ENDPOINT_CLEAR_COMMAND: str = "/api/v1/command"
    
    def __init__(self, server_url: str, api_key: str, timeout: int = 5) -> None:
        super().__init__(server_url, headers={'X-API-Key': api_key}, timeout=timeout)

    def version(self) -> Tuple[bool, Any]:
        return self.get(endpoint=self.ENDPOINT_VERSION, status_codes=[200])
    
    def get_commands(self) -> Tuple[bool, Any]:
        return self.get(endpoint=self.ENDPOINT_GET_COMMANDS, status_codes=[200])
    
    def clear_commands(self) -> Tuple[bool, Any]:    
        return self.delete(endpoint=self.ENDPOINT_CLEAR_COMMANDS, status_codes=[200])

    def clear_command(self, uuid: str) -> Tuple[bool, Any]:    
        data = {"uuid": uuid}
        return self.delete(endpoint=self.ENDPOINT_CLEAR_COMMAND, data=data, status_codes=[200, 204])

