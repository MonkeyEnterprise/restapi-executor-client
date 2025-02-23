##
#
# Copyright (c) 2025, Lorenzo Pouw.
# All rights reserved.
#
##

from .propresenter import ProPresenter
from .server import Server
import logging
import time
import signal

__VERSION__: str = "1.0.0"

class Client:
    def __init__(self, server_url: str, propresenter_url: str, api_key: str, debug: bool) -> None:
        """
        Initializes the ProPresenter client.

        Args:
            server_url (str): URL of the REST API Executor server.
            propresenter_url (str): URL of the ProPresenter server.
            api_key (str): API key for server authentication.
            debug (bool): Enables debug-level logging if True.
        """
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info(f"Initializing ProPresenter client version {__VERSION__}")
        
        self.server = Server(server_url, api_key)
        self.propresenter = ProPresenter(propresenter_url)
        self.shutdown_flag = False  # Flag to handle graceful shutdown

        # Register signal handlers
        signal.signal(signal.SIGINT, self.handle_shutdown)  # Handle Ctrl+C
        signal.signal(signal.SIGTERM, self.handle_shutdown)  # Handle Docker stop

    def handle_shutdown(self, signum, frame):
        """Handles shutdown signals gracefully."""
        logging.info(f"Received shutdown signal ({signum}). Exiting gracefully...")
        self.shutdown_flag = True

    def run(self) -> None:
        """Starts the main loop and handles shutdown gracefully."""
        logging.info("Client started. Press Ctrl+C to stop.")

        try:
            while not self.shutdown_flag:
                self.wait_for_servers_online()
                logging.info("Both servers are online. Executing main script.")
                self.execute_main_script()
        except KeyboardInterrupt:
            logging.info("Manual interruption detected. Shutting down...")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            logging.info("Client has shut down completely.")

    def wait_for_servers_online(self):
        """
        Blocks until both servers are online or a shutdown is requested.
        """
        logging.info("Checking if both servers are online...")
        while not (self.server_online() and self.propresenter_online()):
            if not self.server_online():
                logging.warning("REST API Executor server is offline. Retrying in 5 seconds...")
            if not self.propresenter_online():
                logging.warning("ProPresenter server is offline. Retrying in 5 seconds...")
            if self._should_shutdown():
                return
            time.sleep(5)

        while self.server_online() and self.propresenter_online() and not self.shutdown_flag:
            try:
                logging.info("Main script running.")
                connection_state, data = self.server.get_commands()
                if connection_state and data:
                    for command in data:
                        if isinstance(command, dict):
                            cmd_type = command.get('command')
                            message = command.get('message', '')
                            uuid = command.get('uuid', '')

                            match cmd_type:
                                case 'trigger':
                                    self.propresenter.trigger(
                                        id="parentpager",
                                        token="number",
                                        message=message
                                    )
                                    time.sleep(10) # needs to be variable
                                    self.propresenter.clear(id="parentpager")
                                case 'clear':
                                    self.propresenter.clear(id="parentpager")
                                case _:
                                    logging.warning(f"Unknown command received: {cmd_type}")

                            self.server.clear_commands()
                time.sleep(0.1)
            except Exception as e:
                logging.exception("Error during main script execution:")
                break  # Exit the loop on error
            
            logging.info("One of the servers has gone offline. Rechecking connections...")

    def server_online(self) -> bool:
        """
        Checks if the REST API Executor server is online.

        Returns:
            bool: True if the server is online, False otherwise.
        """
        try:
            return self.server.get_status()[0]
        except Exception as e:
            logging.error(f"Error checking server status: {e}")
            return False

    def propresenter_online(self) -> bool:
        """
        Checks if the ProPresenter server is online.

        Returns:
            bool: True if the server is online, False otherwise.
        """
        try:
            return self.propresenter.version()[0]
        except Exception as e:
            logging.error(f"Error checking ProPresenter server status: {e}")
            return False

    def _should_shutdown(self) -> bool:
        """
        Checks if a shutdown has been requested.

        Returns:
            bool: True if shutdown has been requested, False otherwise.
        """
        if self.shutdown_flag:
            logging.info("Shutdown requested. Stopping server checks.")
            return True
        return False
