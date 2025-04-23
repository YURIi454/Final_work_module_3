import json
import os
from typing import Any

import requests
from dotenv import load_dotenv

from config import ROOT_DIR
from custom_loger import get_logger

logger = get_logger()

load_dotenv(".env")
API_KEY = os.getenv("API_KEY_")


def external_request_api_sp_500() -> Any:
    """Функция выполняет API запросы.
    Для S&P500"""

    logger.info("Запуск")

    result_api = []
    user_stocks = read_user_settings()

    for st in user_stocks["user_stocks"]:
        # try:
        #     url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={st}&apikey={API_KEY}"
        #
        #     headers = {"apikey": API_KEY}
        #
        #     response_currency = requests.get(url, headers=headers)
        #
        #     result_api.append(response_currency.json()["Weekly Time Series"]["2025-03-28"]["3. low"])
        # except Exception as error:
        #     logger.error(f"Ошибка API запроса {error}")
        if st: # для проверки , из-за ограничения количества запросов (код выше раскомментировать, эту строку убрать)
            return 0.0

    result = dict(zip(user_stocks["user_stocks"], result_api))

    return result


def external_request_api_currency() -> Any:
    """Функция выполняет API запросы.
    Для курса валют."""

    logger.info("Запуск")

    result_api = []
    user_stocks = read_user_settings()

    for st in user_stocks["user_currencies"]:
        # try:
        #     url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={st}&apikey={API_KEY}"
        #
        #     headers = {"apikey": API_KEY}
        #
        #     response_currency = requests.get(url, headers=headers)
        #
        #     result_api.append(response_currency.json()["USD"]["Weekly Time Series"]["2025-03-28"]["2. high"])
        # except Exception as error:
        #     logger.error(f"Ошибка API запроса {error}")
        if st: # для проверки , из-за ограничения количества запросов (код выше раскомментировать, эту строку убрать)
            return 0.0

    result = dict(zip(user_stocks["user_currencies"], result_api))

    return result


def read_user_settings() -> dict:
    """Функция читает пользовательские настройки."""

    logger.info("Запуск")
    with open(ROOT_DIR + "/user_settings.json") as file:
        data = dict(json.load(file))

    return data

#
# if __name__ == "__main__":
#     #print(read_user_settings())
#     print(external_request_api_sp_500())
#     print(external_request_api_currency())
