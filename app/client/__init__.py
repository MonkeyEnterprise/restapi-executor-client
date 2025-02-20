##
#
# Copyright (c) 2025, Lorenzo Pouw.
# All rights reserved.
#
##


import logging

__VERSION__: str = "1.0.0"

class Client:
    def __init__(self, host: str, port: int, debug: bool, api_key: str) -> None:
        """Initializes the client."""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f"Initializing propresenter client version {__VERSION__}")

        self.host = host
        self.port = port
        self.debug = debug
        self.api_key = api_key
        
    def run(self) -> None:
        """Starts the client."""
        ...
