import datetime
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.reports import spending_by_category
from src.requests_api import external_request_api_currency, external_request_api_sp_500, read_user_settings
from src.services import categories_of_best_cashback, search_by_names, search_by_phone_numbers, simple_search
from src.views import get_greeting, top_transactions
from tests.conftest import excel_data


@pytest.mark.parametrize(
    "test_time, test_text",
    [
        (datetime.datetime(2023, 3, 20, 7, 15, 45), "Доброе утро! Пользователь!"),
        (datetime.datetime(2023, 5, 24, 14, 3, 45), "Добрый день! Пользователь!"),
        (datetime.datetime(2023, 6, 11, 19, 22, 45), "Добрый вечер! Пользователь!"),
        (datetime.datetime(2023, 1, 10, 1, 31, 45), "Доброй ночи! Пользователь!"),
    ],
)
def test_get_greeting(test_time: str, test_text: str) -> None:
    """Тест приветствия, в зависимости от времени суток."""

    assert get_greeting(test_time) == test_text


def test_top_transactions(excel_data: list[dict]) -> None:
    """Тест вывода топ-5 транзакций."""

    data = top_transactions(pd.DataFrame(excel_data))
    assert data == [
        {
            "amount": 115909.42,
            "category": "Переводы",
            "date": "24.01.2018",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {"amount": 9700.0, "category": "Пополнения", "date": "25.01.2018", "description": "Перевод с карты"},
        {"amount": 5748.0, "category": "Авиабилеты", "date": "25.01.2018", "description": "Aviacassa"},
        {"amount": 840.3, "category": "Ж/д билеты", "date": "24.01.2018", "description": "РЖД"},
        {"amount": 376.0, "category": "Транспорт", "date": "25.01.2018", "description": "Яндекс Такси"},
    ]


@patch("requests.get")
def test_external_request_api_currency(requests_mock: Any) -> None:
    """Тест получения курса валюты по API"""
    requests_mock.return_value.status_code = 200
    requests_mock.return_value.json.return_value = {
        "USD": {"Weekly Time Series": {"2025-03-28": {"2. high": 1.887787}}}
    }
    data = external_request_api_currency()
    assert data == {"USD": 1.887787}


@patch("requests.get")
def test_external_request_api_sp_500(requests_mock: Any) -> None:
    """Тест функции получения стоимости акций."""
    requests_mock.return_value.status_code = 200
    requests_mock.return_value.json.return_value = {"Weekly Time Series": {"2025-03-28": {"3. low": 32.223}}}
    data = external_request_api_sp_500()
    assert data == {"AAPL": 32.223, "AMZN": 32.223, "GOOGL": 32.223, "MSFT": 32.223, "TSLA": 32.223, "S&P500": 32.223}

    requests_mock.return_value.status_code = 200
    requests_mock.return_value.json.return_value = {"Weekly Time Series": {"2025-03-28": {"3. low": 32.223}}}


def test_read_user_settings() -> None:
    """Тест чтения пользовательских настроек."""

    assert read_user_settings() == {
        "user_currencies": ["USD"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA", "S&P500"],
    }


def test_spending_by_category(excel_data: list[dict]) -> None:
    """Тест поиска по категориям."""

    data = spending_by_category(pd.DataFrame(excel_data), "Фастфуд", "2018-01-24 13:59:06")
    assert data == (
        '[{"Дата операции": "2018-01-24 13:59:06", "Дата платежа": "26.01.2018", '
        '"Номер карты": "*7197", "Статус": "OK", "Сумма операции": -325.0, "Валюта '
        'операции": "RUB", "Сумма платежа": -325.0, "Валюта платежа": "RUB", '
        '"Кэшбэк": null, "Категория": "Фастфуд", "MCC": 5814.0, "Описание": "OOO '
        'Frittella", "Бонусы (включая кэшбэк)": 6, "Округление на инвесткопилку": 0, '
        '"Сумма операции с округлением": 325.0}]'
    )


def test_categories_of_best_cashback(dict_data: list[dict]) -> None:
    """Тест категории кэшбэка."""

    data = categories_of_best_cashback(dict_data, "2018", "02")
    assert data == '{"Супермаркеты": 20.0, "Фастфуд": 50.0, "Красота": 1.0}'


def test_simple_search(dict_data: list[dict]) -> None:
    """Тест простой поиск."""

    data = simple_search(dict_data, "OOO Frittella")
    assert data == (
        '[{"date of operation": "12.02.2018 12:40:34", "date of currency": '
        '"14.02.2018", "card number": "*7197", "status": "OK", "operation": {"add": '
        '-314.0, "currency": "RUB"}, "add": -314.0, "currency": "RUB", "cashback": '
        '50.0, "category": "Фастфуд", "description": "OOO Frittella", "Investment '
        'bank": 0, "add with round": 314.0}]'
    )


def test_search_by_phone_numbers(dict_data: list[dict]) -> None:
    """Тест поиск по номеру."""

    data = search_by_phone_numbers(dict_data)
    assert data == (
        '[{"date of operation": "12.02.2017 17:47:21", "date of currency": '
        '"14.02.2018", "card number": "*7197", "status": "OK", "operation": {"add": '
        '-98.41, "currency": "RUB"}, "add": -98.41, "currency": "RUB", "cashback": '
        '20.0, "category": "Супермаркеты", "description": "+7 999 888-77-66", '
        '"Investment bank": 0, "add with round": 98.41}]'
    )


def test_search_by_names(dict_data: list[dict]) -> None:
    """Тест поиск по имени."""

    data = search_by_names(dict_data, "арн")
    assert data == (
        '[{"date of operation": "11.02.2019 15:15:25", "date of currency": '
        '"13.02.2018", "card number": "*7197", "status": "OK", "operation": {"add": '
        '-145.0, "currency": "RUB"}, "add": -145.0, "currency": "RUB", "cashback": '
        '1.0, "category": "Красота", "description": "Арнольд Ш.", "Investment bank": '
        '0, "add with round": 145.0}]'
    )
