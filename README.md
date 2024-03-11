## Build for production

(Based on [this](https://flask.palletsprojects.com/en/2.3.x/tutorial/deploy/))

### Build distro
`python3 -m build --wheel`

### Install dependencies

Copy dist dir to production server.

Create new virtual env
```shell
python3 -m venv venv
```
and activate this env
```shell
source venv/bin/activate
```

Then install all required dependencies from `dist/{packageName}.whl`
```shell
pip3 install dist/AI_fairytale-1.0-py3-none-any.whl
```

Install production server like Waitress for example.
```shell
pip3 install waitress
```

Copy systemd unit (`services/ai_fairytale.service`) to production server `/etc/systemd/system/`.

Then enable it
```shell
sudo systemctl enable ai_fairytale
```
and start it
```shell
sudo systemctl start ai_fairytale
```

### Install reverse proxy

Install Caddy.

Copy Caddyfile (`services/Caddyfile`) to production server and run `caddy reload` from directory containing Caddyfile.
