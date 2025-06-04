from prometheus_client import start_http_server, Counter

# Определение метрики
BOT_COMMANDS_COUNTER = Counter(
    'telegram_bot_commands_total',
    'Total number of Telegram bot commands',
    ['command']
)


def increment_command_metric(command_name: str):
    BOT_COMMANDS_COUNTER.labels(command=command_name).inc()

# Запуск сервера 
def start_metrics_server():
    print("[metrics] Exporter started on :8000")
    start_http_server(8000)
