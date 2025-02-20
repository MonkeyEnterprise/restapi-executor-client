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
    """Parses command-line arguments for configuring the Flask server.

    Returns:
        argparse.Namespace: An object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Start the Flask API server.")
    
    parser.add_argument("--server_url", type=str, default=os.getenv("SERVER_URL", "http://127.0.0.1:80"), help="REST API Server URL")
    parser.add_argument("--propresenter_url", type=str, default=os.getenv("PROPRESENTER_URL", "http://127.0.0.1:5000"), help="ProPresenter URL")
    parser.add_argument("--api_key", type=str, default=os.getenv("API_KEY", "your_secret_api_key"), help="API Key")
    parser.add_argument("--debug", action="store_true", default=os.getenv("DEBUG", "False").lower() in ["true", "1"], help="Enable debug logging")

    args, _ = parser.parse_known_args()
    
    return args

if __name__ == "__main__":
    args = get_args()
    server = Client(server_url=args.server_url, propresenter_url=args.propresenter_url, api_key=args.api_key, debug=args.debug)
    server.run()
