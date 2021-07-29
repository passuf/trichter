# Trichter
## Disclaimer
This project is currently work in progress. Only use at your own risk.

## Prerequisites
- You need a server with a public IP address.
- You need to configure two DNS entries:
  - One for the `trichter` server, e.g. `trichter.io`
  - One for the tunnels, e.g. `*.trichter.io`
- You need a client which is able to connect to the server via SSH.


## Installation
### Server
1. Create a symlink for `trichter`: `sudo ln -s /path/to/trichter/main.py /usr/local/bin/trichter`
1. Download the `caddy` release for your system and store the binary in `./bin/caddy`.
1. Make sure that `trichter` can bind to port 80 and 443, e.g. with `setcap`: `sudo setcap 'cap_net_bind_service=+ep' ./bin/caddy`
1. Run the server: `trichter server run`

### Client
1. Create a symlink for `trichter`: `sudo ln -s /path/to/trichter/main.py /usr/local/bin/trichter`
1. Assuming you want to expose a local application running on port 8080 and you want to expose it using the domain test.trichter.io, run `trichter tunnel --port 8080 --domain test.trichter.io --server trichter.io`


## Acknowledgements
- [Anders Pitman](https://github.com/anderspitman), who inspiried this project with [SirTunnel](https://github.com/anderspitman/SirTunnel).
- [Caddy](https://github.com/caddyserver/caddy), which powers the proxy server with automatic HTTPS.