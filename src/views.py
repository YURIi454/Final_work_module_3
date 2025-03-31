import datetime
from typing import Any

import pandas as pd

from config import PATH_XLSX
from custom_loger import get_logger
from src.file_handler import xlsx_handler
from src.requests_api import external_request_api_currency, external_request_api_sp_500

logger = get_logger()


def get_greeting(date_now=datetime.datetime.now()) -> Any:
    """Функция приветствия страницы главная.
    Возвращает JSON-файл с ответом."""

    logger.info("Запуск.")

    user_name = "Пользователь"
    hello_user = ""

    if 6 >= date_now.hour > 0:
        hello_user = "Доброй ночи!"
    if 6 < date_now.hour <= 12:
        hello_user = "Доброе утро!"
    if 12 < date_now.hour <= 18:
        hello_user = "Добрый день!"
    if 18 < date_now.hour <= 23:
        hello_user = "Добрый вечер!"

    return f"{hello_user} {user_name}!"


def return_courses() -> Any:
    """Ответ API запроса.
    Курсы валют и акций."""

    logger.info("Запуск.")

    course_currency = external_request_api_currency()
    user_settings = external_request_api_sp_500()

    return course_currency, user_settings


def card_number(transactions: pd.DataFrame) -> Any:
    """Последние 4 цифры карты.
    Общая сумма расходов;
    Кэшбэк."""

    logger.info("Запуск.")

    cards_list = []

    add_group_data = transactions.groupby("Номер карты").agg({"Сумма операции с округлением": "sum", "Кэшбэк": "sum"})
    for c_number, row in add_group_data.iterrows():
        inform_to_card = {
            "last_digits": str(c_number)[-4:],
            "total_spent": float(row["Сумма операции с округлением"]),
            "cashback": float(row["Кэшбэк"]),
        }
        cards_list.append(inform_to_card)

    return cards_list


def top_transactions(transactions: pd.DataFrame) -> Any:
    """Выводит пять самых крупных транзакций"""

    logger.info("Запуск.")

    best_transaction = []

    best_data = transactions.sort_values(by="Сумма операции с округлением", ascending=False).head(5)
    for data, row in best_data.iterrows():
        best_transaction.append(
            {
                "date": row["Дата платежа"],
                "amount": float(row["Сумма операции с округлением"]),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    return best_transaction


def main_page(date: Any) -> dict:
    """Функция главной страницы."""

    struct_file_json = card_number(xlsx_handler(PATH_XLSX))
    json_response = {
        "greeting": get_greeting(date),
        "cards": card_number(struct_file_json),
        "top_transactions": top_transactions(struct_file_json),
        "currency_rates": external_request_api_currency(),
        "stock_prices": external_request_api_sp_500(),
    }
    return json_response
