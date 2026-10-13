#!/usr/bin/env python3
"""Watch Keelson records in a local browser; no third-party packages required."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).with_suffix('')))
from server import make_server
from dashboard_setup import default_registry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry', default=default_registry(), type=Path)
    parser.add_argument('--port', type=int, default=0)
    args = parser.parse_args()
    server = make_server(args.registry, args.port)
    print(f'http://127.0.0.1:{server.server_port}/#token={server.token}', flush=True)
    print('Read-only. Collects every 2 seconds while this process and machine are running. Ctrl+C stops.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__': main()
