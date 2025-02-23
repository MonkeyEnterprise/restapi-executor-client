##
#
# Copyright (c) 2025, Lorenzo Pouw.
# All rights reserved.
#
##

from client import Client
import os
import argparse

def get_args() -> argparse.Namespace:
    """
    Parses command-line arguments for configuring the client.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Start the ProPresenter client.")

    # Define command-line arguments with defaults from environment variables
    parser.add_argument(
        "--server_url",
        type=str,
        default=os.getenv("SERVER_URL", "http://localhost:80"),
        help="REST API Server URL (default from SERVER_URL environment variable)."
    )
    parser.add_argument(
        "--propresenter_url",
        type=str,
        default=os.getenv("PROPRESENTER_URL", "http://localhost:5000"),
        help="ProPresenter Server URL (default from PROPRESENTER_URL environment variable)."
    )
    parser.add_argument(
        "--api_key",
        type=str,
        default=os.getenv("API_KEY", "test"),
        help="API Key for server authentication (default from API_KEY environment variable)."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=os.getenv("DEBUG", "False").lower() in ["true", "1"],
        help="Enable debug-level logging (default from DEBUG environment variable)."
    )

    # Parse the known arguments
    args, _ = parser.parse_known_args()
    return args

if __name__ == "__main__":
    # Parse command-line arguments
    args = get_args()

    # Initialize the Client with the provided arguments
    server = Client(
        server_url=args.server_url,
        propresenter_url=args.propresenter_url,
        api_key=args.api_key,
        debug=args.debug
    )

    # Run the client
    server.run()
