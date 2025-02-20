##
#
# Copyright (c) 2025, Lorenzo Pouw.
# All rights reserved.
#
##


import logging
import requests
import time
import signal

__VERSION__: str = "1.0.0"

class Client:
    def __init__(self, server_url: str, propresenter_url: str, api_key: str, debug: bool = False) -> None:
        """Initializes the client."""
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info(f"Initializing ProPresenter client version {__VERSION__} with debug={debug}")

        self.server_url = server_url
        self.pp_url = propresenter_url
        self.api_key = api_key
        self.debug = debug
        self.shutdown_flag = False  # Flag to handle graceful shutdown

        # Setup headers with API key for requests
        self.headers = {'X-API-Key': self.api_key}

        # Register signal handlers
        signal.signal(signal.SIGINT, self.handle_shutdown)  # Handle Ctrl+C
        signal.signal(signal.SIGTERM, self.handle_shutdown)  # Handle Docker stop

    def handle_shutdown(self, signum, frame):
        """Handles shutdown signals gracefully."""
        logging.info(f"Received shutdown signal ({signum}). Exiting gracefully...")
        self.shutdown_flag = True

    def run(self) -> None:
        """Starts the client."""
        logging.info("Client started. Press Ctrl+C to stop.")
        while not self.shutdown_flag:
            self.check()
            time.sleep(5)

        logging.info("Client shutdown complete.")

    def check(self) -> None:
        """Checks the server status and retrieves data."""
        try:
            url = f"{self.server_url}/api/v1"
            logging.debug(f"Sending request to: {url} with headers: {self.headers}")

            response = requests.get(url, headers=self.headers, timeout=5)
            logging.debug(f"Received response: {response.status_code} {response.reason}")

            if response.status_code == 200:
                logging.info("Successfully fetched data.")
                logging.debug(f"Response Headers: {response.headers}")
                logging.debug(f"Response Body: {response.text}")
                return response.json()
            else:
                logging.error(f"Server error: {response.status_code} - {response.text}")

        except requests.exceptions.Timeout:
            logging.error("Request timeout occurred.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")

        return []
