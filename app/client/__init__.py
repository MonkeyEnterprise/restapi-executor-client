##
#
# Copyright (c) 2025, Lorenzo Pouw.
# All rights reserved.
#
##


import logging
import time
import signal
from typing import Tuple, Any
from .api_propresenter import ProPresenterAPI
from .api_executor import ExecutorAPI

class Client:
    
    VERSION: str = "1.0.0"
    
    def __init__(self, server_url: str, propresenter_url: str, api_key: str, timeout: int, poll_time: int, debug: bool) -> None:
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info(f"Initializing ProPresenter client version {self.VERSION}")
        
        self.executor_api = ExecutorAPI(server_url, api_key)
        self.propresenter = ProPresenterAPI(propresenter_url)
        self.timeout = timeout
        self.poll_time = poll_time
        self.shutdown_flag = False

        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def run(self) -> None:
        logging.info("Client started. Press Ctrl+C to stop.")
        try:
            self._wait_for_servers()
            logging.info("Both servers are online. Starting main script execution.")

            while not self.shutdown_flag:
                try:
                    connection_state, data = self.executor_api.get_commands()

                    if connection_state and isinstance(data, list):
                        for command in data:
                            if isinstance(command, dict):
                                cmd_type = command.get('command')
                                uuid = command.get('uuid', '')

                                logging.debug(f"Processing command: {cmd_type} with UUID: {uuid}")

                                match cmd_type:
                                    case 'trigger':
                                        self._handle_trigger_command(command, uuid)
                                    case 'clear':
                                        self._handle_clear_command(command, uuid)
                                    case _:
                                        logging.warning(f"Unknown command received: {cmd_type}")

                    time.sleep(self.poll_time)

                except Exception as e:
                    logging.exception("Error during main script execution:")
                    break

        except KeyboardInterrupt:
            logging.info("Manual interruption detected. Shutting down...")
        finally:
            logging.info("Client has shut down completely.")

    def _handle_trigger_command(self, data: dict, uuid: str) -> None:
        try:
            message = data.get("message", {})
            if not isinstance(message, dict):
                logging.error(f"Invalid 'message' format. UUID: {uuid}")
                return

            message_id = str(message.get('id', '')).strip()
            message_token = str(message.get('token', '')).strip()
            message_content = str(message.get('content', '')).strip()
            message_duration = message.get('duration')

            if not message_id or not message_token or not message_content or not isinstance(message_duration, (int, float)) or message_duration <= 0:
                logging.error("Invalid message data received.")
                return

            logging.info(f"Triggering message: {message_content} with ID: {message_id}")
            self.propresenter.trigger(id=message_id, token=message_token, message=message_content)

            time.sleep(int(message_duration))  

            self.propresenter.clear(id=message_id)
            self.executor_api.clear_command(uuid)

        except Exception as e:
            logging.exception("Error processing trigger command.")

    def _handle_clear_command(self, data: dict, uuid: str) -> None:
        try:
            message = data.get("message", {})
            if not isinstance(message, dict):
                logging.error(f"Invalid 'message' format. UUID: {uuid}")
                return

            message_id = message.get('id', '').strip()
            if not message_id:
                logging.error("Invalid message ID.")
                return

            logging.info(f"Clearing message with ID: {message_id}")
            self.propresenter.clear(id=message_id)
            self.executor_api.clear_commands()

        except Exception as e:
            logging.exception("Error processing clear command.")

    def _wait_for_servers(self):
        logging.info("Checking if both servers are online...")
        while not (self._executor_api_online() and self._propresenter_online()):
            logging.warning("Waiting for servers to come online...")
            time.sleep(self.timeout)
        logging.info("Both servers are now online.")

    def _executor_api_online(self) -> bool:
        try:
            return self.executor_api.version()[0]
        except Exception as e:
            logging.error(f"Error checking ExecutorAPI server status: {e}")
            return False

    def _propresenter_online(self) -> bool:
        try:
            success, data = self.propresenter.version()
            logging.error(f"{success}, {data}")
            return success and isinstance(data, dict)
        except Exception as e:
            logging.error(f"Error checking ProPresenter server status: {e}")
            return False

    def _handle_shutdown(self, signum, frame):
        logging.info(f"Received shutdown signal ({signum}). Exiting gracefully...")
        self.shutdown_flag = True
