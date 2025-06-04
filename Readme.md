# Telegram Bot with Yandex GPT

This is a simple Telegram bot that integrates with Yandex GPT API to generate AI-powered responses to user messages.

In addition, there is a special test which is aimed to determine the psychological state of a person.

## Features
- Sends user messages to Yandex GPT API.
- Returns AI-generated responses.
- Works continuously using Telegram's long polling.
- Determining the psychological state of a person

## Requirements
- Python 3.7+
- Telegram Bot API token
- Yandex GPT API key

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/telegram-yandex-gpt-bot.git
   cd telegram-yandex-gpt-bot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up your API keys:
   - Replace `your_telegram_bot_token` in the script with your Telegram bot token.
   - Replace `your_yandex_gpt_api_key` with your Yandex GPT API key.

## Usage

Firstly, you should run Prometheus server:

```sh
./prometheus --config.file=prometheus.yml
```

Run the bot with (It'll start custom Prometheus exportet + Telegram bot):
```sh
python3 bot.py
```

```csharp
[Telegram бот + Prometheus клиент]
         |
         |  (start_http_server на :8000)
         V
http://localhost:8000/metrics
         ↑
         |  (scrape по расписанию)
[Prometheus сервер] <--- prometheus.yml
         |
         V
[Grafana] (вытягивает данные из Prometheus)
```

After that, the monitoring is available on:
1) ```http://localhost:9000``` - Web UI prometheus
2) ```http://localhost:3000``` - Web UI Grafana (prefered)

The bot will start listening for messages and responding with AI-generated replies.

## Dependencies
- `pyTelegramBotAPI` – Telegram bot framework
- `requests` – HTTP requests library

## License
This project is open-source and available under the MIT License.

## Author
Igor Stovba

Alexander Sizov

