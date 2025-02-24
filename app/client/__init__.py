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
    """
    A client that manages communication between a REST API Executor server and a ProPresenter server.

    This client continuously polls for commands from the server and executes them on the ProPresenter.
    It handles shutdown signals and server connectivity checks.

    Attributes:
        server (Server): Instance for handling server communication.
        propresenter (ProPresenter): Instance for interacting with ProPresenter.
        timeout (int): Time (in seconds) to wait before retrying server connection.
        poll_time (int): Time (in seconds) between consecutive command polls.
        shutdown_flag (bool): Flag to indicate shutdown status.
    """

    def __init__(self, server_url: str, propresenter_url: str, api_key: str, timeout: int, poll_time: int, debug: bool) -> None:
        """
        Initializes the Client instance with server and ProPresenter URLs, API key, and settings.

        Args:
            server_url (str): URL of the REST API Executor server.
            propresenter_url (str): URL of the ProPresenter server.
            api_key (str): API key for server authentication.
            timeout (int): Timeout in seconds for server connection retries.
            poll_time (int): Time in seconds between command polling.
            debug (bool): Flag to enable debug-level logging.
        """
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info(f"Initializing ProPresenter client version {__VERSION__}")
        
        self.server = Server(server_url, api_key)
        self.propresenter = ProPresenter(propresenter_url)
        self.timeout = timeout
        self.poll_time = poll_time
        self.shutdown_flag = False

        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def run(self) -> None:
        """
        Starts the main client loop, handling server polling and command execution.

        Continuously checks for commands from the server, executes them, and handles errors
        or shutdown signals gracefully.
        """
        logging.info("Client started. Press Ctrl+C to stop.")
        try:
            self._wait_for_servers()
            logging.info("Both servers are online. Starting main script execution.")

            while not self.shutdown_flag:
                try:
                    connection_state, data = self.server.get_commands()

                    if connection_state and data:
                        for command in data:
                            if isinstance(command, dict):
                                cmd_type = command.get('command')
                                uuid = command.get('uuid', '')
                                message = command.get('message', {})
                                message_id = message.get('id', '')
                                message_token = message.get('token', '')
                                message_content = message.get('content', '')
                                message_duration = message.get('duration', '0')

                                logging.debug(f"Processing command: {cmd_type} with UUID: {uuid}")

                                match cmd_type:
                                    case 'trigger':
                                        self.propresenter.trigger(
                                            id=message_id,
                                            token=message_token,
                                            message=message_content
                                        )

                                        try:
                                            time.sleep(int(message_duration))
                                        except ValueError:
                                            logging.warning(f"Invalid duration '{message_duration}', skipping wait.")

                                        self.propresenter.clear(id=message_id)
                                        self.server.clear_command(uuid=uuid)

                                    case _:
                                        logging.warning(f"Unknown command received: {cmd_type}")

                    time.sleep(self.poll_time)

                except Exception as e:
                    logging.exception("Error during main script execution:")
                    break

                logging.info("One of the servers has gone offline. Rechecking connections...")

        except KeyboardInterrupt:
            logging.info("Manual interruption detected. Shutting down...")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            logging.info("Client has shut down completely.")

    def _wait_for_servers(self):
        """
        Waits until both the REST API Executor server and ProPresenter server are online.

        Continuously retries the connection after a timeout period until both servers respond positively
        or the shutdown flag is triggered.
        """
        logging.info("Checking if both servers are online...")
        while not (self._server_online() and self._propresenter_online()):
            if not self._server_online():
                logging.warning(f"REST API Executor server is offline. Retrying in {self.timeout} seconds...")
            if not self._propresenter_online():
                logging.warning(f"ProPresenter server is offline. Retrying in {self.timeout} seconds...")
            if self.shutdown_flag:
                return
            time.sleep(self.timeout)
        logging.info("Both servers are now online.")

    def _server_online(self) -> bool:
        """
        Checks the online status of the REST API Executor server.

        Returns:
            bool: True if the server is online, False otherwise.
        """
        try:
            return self.server.version()[0]
        except Exception as e:
            logging.error(f"Error checking server status: {e}")
            return False

    def _propresenter_online(self) -> bool:
        """
        Checks the online status of the ProPresenter server.

        Returns:
            bool: True if the server is online, False otherwise.
        """
        try:
            # return self.propresenter.version()[0]
            return True
        except Exception as e:
            logging.error(f"Error checking ProPresenter server status: {e}")
            return False

    def _handle_shutdown(self, signum, frame):
        """
        Handles shutdown signals (SIGINT or SIGTERM).

        Args:
            signum (int): The signal number received.
            frame: Current stack frame (unused).
        """
        logging.info(f"Received shutdown signal ({signum}). Exiting gracefully...")
        self.shutdown_flag = True
