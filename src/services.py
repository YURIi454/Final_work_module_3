import json
import re

from pandas import read_excel

from config import PATH_XLSX
from custom_loger import get_logger

logger = get_logger()


def categories_of_best_cashback(transactions: list[dict], year: str, month: str) -> str:
    """Выгодные категории повышенного кешбэка.
    Выводит JSON с анализом, сколько на каждой
    категории можно заработать кешбэка."""

    logger.info("Запуск")

    best_cashback = {}

    for i in transactions:
        if i.get("cashback") and ((i["date of currency"])[6:] == year) and ((i["date of currency"])[3:5] == month):
            best_cashback[i["category"]] = i["cashback"]

    return json.dumps(best_cashback, ensure_ascii=False)


def simple_search(transactions: list[dict], find_word: str) -> str:
    """Простой поиск.
    Выводит JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""

    logger.info("Запуск")

    result_search = []

    for i in transactions:
        if i.get("description") == find_word:
            result_search.append(i)

    return json.dumps(result_search, ensure_ascii=False)


def search_by_phone_numbers(transactions: list[dict]) -> str:
    """Поиск по телефонным номерам.
    Выводит JSON со всеми транзакциями,
    содержащими в описании мобильные номера."""

    logger.info("Запуск")

    result_search = []

    for i in transactions:
        if re.search(r"\d \d{3} \d{3}", i["description"]):
            result_search.append(i)

    return json.dumps(result_search, ensure_ascii=False)


def search_by_names(transactions: list[dict], find_names: str) -> str:
    """Поиск переводов физическим лицам.
    Выводит JSON со всеми транзакциями, которые относятся к
    переводам физическим лицам."""

    logger.info("Запуск")

    result_search = []

    for i in transactions:
        if find_names.title() in i["description"] and "." in i["description"]:
            result_search.append(i)

    return json.dumps(result_search, ensure_ascii=False)
