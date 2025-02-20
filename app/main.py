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
    
    parser.add_argument("--host", type=str, default=os.getenv("HOST", "127.0.0.1"), help="Host IP address")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", 80)), help="Port number")
    parser.add_argument("--api_key", type=str, default=os.getenv("API_KEY", ""), help="API Key")
        
    debug_env = os.getenv("DEBUG", "False").lower()
    debug_default = debug_env in {"1", "true", "yes"}
    parser.add_argument("--debug", action="store_true", default=debug_default, help="Enable debug mode")
    args, _ = parser.parse_known_args()
    
    return args

if __name__ == "__main__":
    args = get_args()
    server = Client(host=args.host, port=args.port, debug=args.debug, api_key=args.api_key)
    server.run()

