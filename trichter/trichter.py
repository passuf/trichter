import json
import time
import uuid
import subprocess
import random
from urllib import request


class TrichterServer:
    caddy_host: str
    caddy_port: int
    caddy_config: str

    def __init__(self, caddy_host: str, caddy_port: int, caddy_config: str):
        self.caddy_host = caddy_host
        self.caddy_port = caddy_port
        self.caddy_config = caddy_config

    def setup(self):
        raise NotImplemented('Automatic server setup is not yet implemented.')

    def run(self, caddy_binary='./bin/caddy'):
        subprocess.run([caddy_binary, 'run', '--config', self.caddy_config])

    def create_tunnel(self, port, domain):
        # TODO: Check if port is available

        tunnel_id = str(uuid.uuid4())
        print(f'Creating tunnel {tunnel_id} - {domain}')

        body = {
            "@id": tunnel_id,
            "match": [{
                "host": [domain],
            }],
            "handle": [{
                "handler": "reverse_proxy",
                "upstreams": [{
                    "dial": ':' + str(port)
                }]
            }]
        }

        url = f'http://{self.caddy_host}:{self.caddy_port}/config/apps/http/servers/trichter/routes'
        self.__send_caddy_request__('POST', url, body)

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.delete_tunnel(tunnel_id)
                break

    def delete_tunnel(self, tunnel_id):
        print(f'Deleting tunnel {tunnel_id}')

        url = f'http://{self.caddy_host}:{self.caddy_port}/id/{tunnel_id}'
        self.__send_caddy_request__('DELETE', url)

    @staticmethod
    def __send_caddy_request__(method: str, url: str, body: dict = None, headers: dict = None):
        if body is None:
            body = {}

        if headers is None:
            headers = {'Content-Type': 'application/json'}

        body = json.dumps(body).encode('utf-8')
        r = request.Request(method=method, url=url, headers=headers)

        return request.urlopen(r, body)


class TrichterClient:
    server: str
    trichter_command: str

    def __init__(self, server, trichter_command='trichter'):
        self.server = server
        self.trichter_command = trichter_command

    def create_tunnel(self, port, domain):
        remote_port = random.randint(40000, 65000)

        result = subprocess.run(
            ['ssh', '-tR', f'{remote_port}:localhost:{port}', self.server,
             self.trichter_command, 'server', 'tunnel', '--port', str(remote_port), '--domain', domain],
            capture_output=True, text=True
        )
        print(result.stdout, result.stderr)