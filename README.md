# NASA Picture of the Day — Telegram Bot

Fetches the Astronomy Picture of the Day from NASA, translates the title and
explanation into Russian via Yandex Cloud, and publishes it to a Telegram
channel on a daily schedule.

## Project layout

    nasa_potd/            bot package
      __main__.py         entry point (python -m nasa_potd)
      nasa.py             APOD API client
      translator.py       Yandex Translate client
      telegram.py         Telegram Bot API client
      message.py          message text assembly
      config.py           settings: translation, notifications, proxy
    tests/                unit tests (python -m unittest discover tests)
    deploy/               systemd unit, timer and bot-env.sh for the server
    .env.example          environment variables template
    requirements.txt      dependencies
    LICENSE               MIT license

## Configuration

`nasa_potd/config.py`:

| Option                 | Default | Description                                |
|------------------------|---------|--------------------------------------------|
| `translate`            | `True`  | translate title and explanation to Russian |
| `translate_from`       | `'en'`  | source language                            |
| `translate_to`         | `'ru'`  | target language                            |
| `disable_notification` | `False` | publish silently in the channel            |
| `proxy`                | `None`  | proxy for the NASA API request             |

The proxy is disabled by default. To enable it, set the address in
`config.py`, for example for a SOCKS proxy:

    proxy = 'socks5h://user:pass@host:1080'

SOCKS proxies require the `requests[socks]` dependency (already listed in
`requirements.txt`). The proxy applies only to the NASA API request; to route
all outgoing traffic through a proxy, use the standard environment variables
(`ALL_PROXY` etc.) — `requests` picks them up automatically.

## Environment variables

| Variable       | Purpose                          |
|----------------|----------------------------------|
| `BOT_TOKEN`    | Telegram bot token               |
| `CHAT_ID`      | ID of the channel to publish to  |
| `YC_API_TOKEN` | Yandex Cloud Translate API key   |

Locally the values are read from `.env` (python-dotenv); on the server they
come from `bot-env.sh` via `EnvironmentFile=` in the systemd unit.

## Local run

    python -m venv .venv
    .venv/bin/pip install -r requirements.txt
    cp .env.example .env
    .venv/bin/python -m nasa_potd

## Tests

    .venv/bin/python -m unittest discover tests

## Deployment

The project lives in `/opt/bot/nasa_potd` (code and venv together; the path is
hard-coded in the unit and `bot-env.sh`):

    rsync -a --exclude .venv --exclude .env ./ server:/opt/bot/nasa_potd/
    /opt/bot/nasa_potd/bin/pip install -r /opt/bot/nasa_potd/requirements.txt
    cp deploy/nasa-bot.service deploy/nasa-bot.timer /etc/systemd/system/
    cp deploy/bot-env.sh /opt/bot/nasa_potd/bot-env.sh
    systemctl daemon-reload
    systemctl enable --now nasa-bot.timer

If the server has no direct access to the NASA API, enable `proxy` in
`nasa_potd/config.py` on the server.

Manual run and logs:

    systemctl start nasa-bot.service
    journalctl -u nasa-bot.service

## License

MIT — see [LICENSE](LICENSE).
