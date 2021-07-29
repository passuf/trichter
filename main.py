#!/usr/bin/env python3

import argparse

from trichter.trichter import TrichterServer, TrichterClient


def server_setup(args):
    trichter_server = TrichterServer(args.caddy_host, args.caddy_port, args.caddy_config)
    trichter_server.setup()


def server_run(args):
    trichter_server = TrichterServer(args.caddy_host, args.caddy_port, args.caddy_config)
    trichter_server.run(caddy_binary=args.caddy_binary)


def server_tunnel(args):
    trichter_server = TrichterServer(args.caddy_host, args.caddy_port, args.caddy_config)
    trichter_server.create_tunnel(port=args.port, domain=args.domain, http_basic_user=args.http_basic_user,
                                  http_basic_password=args.http_basic_password)


def tunnel(args):
    trichter_client = TrichterClient(server=args.server, trichter_command=args.trichter_command)
    trichter_client.create_tunnel(port=args.port, domain=args.domain, http_basic_user=args.http_basic_user,
                                  http_basic_password=args.http_basic_password)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='target', required=True)

    # trichter tunnel --port 9000 --domain test.trichter.io --server trichter.io
    client_parser = subparsers.add_parser('tunnel')
    client_parser.add_argument('-p', '--port', type=int, required=True, help='Local port to tunnel')
    client_parser.add_argument('-d', '--domain', type=str, required=True, help='Domain to use for the tunnel')
    client_parser.add_argument('-s', '--server', type=str, required=True, help='Trichter server to use')
    client_parser.add_argument('--http_basic_user', type=str, required=False, help='HTTP Basic Auth user')
    client_parser.add_argument('--http_basic_password', type=str, required=False, help='HTTP Basic Auth password hash')
    client_parser.add_argument('--trichter_command', default='trichter', type=str, help='Trichter command to execute')

    server_parser = subparsers.add_parser('server')
    server_parser.add_argument('--caddy_host', default='127.0.0.1', type=str, help='Caddy host to use')
    server_parser.add_argument('--caddy_port', default=2019, type=int, help='Caddy port to use')
    server_parser.add_argument('--caddy_config', default='caddy_config.json', type=str, help='Caddy config to use')

    server_subparsers = server_parser.add_subparsers(dest='action', required=True)

    # trichter server setup
    server_setup_parser = server_subparsers.add_parser('setup')

    # trichter server run
    server_run_parser = server_subparsers.add_parser('run')
    server_run_parser.add_argument('--caddy_binary', default='./bin/caddy', type=str, help='Path to Caddy binary')

    # trichter server tunnel --port 40001 --domain test.trichter.io
    server_tunnel_parser = server_subparsers.add_parser('tunnel')
    server_tunnel_parser.add_argument('-p', '--port', type=int, required=True, help='Local port to tunnel')
    server_tunnel_parser.add_argument('-d', '--domain', type=str, required=True, help='Domain to use for the tunnel')
    server_tunnel_parser.add_argument('--http_basic_user', type=str, required=False, help='HTTP Basic Auth user')
    server_tunnel_parser.add_argument('--http_basic_password', type=str, required=False,
                                      help='HTTP Basic Auth password hash')

    args = parser.parse_args()
    if args.target == 'tunnel':
        tunnel(args)
    elif args.target == 'server' and args.action == 'setup':
        server_setup(args)
    elif args.target == 'server' and args.action == 'run':
        server_run(args)
    elif args.target == 'server' and args.action == 'tunnel':
        server_tunnel(args)
    else:
        parser.print_usage()
