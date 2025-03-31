from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from custom_loger import get_logger
from src.decorator import log

logger = get_logger()


@log("reports_log")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Траты по категории
    Функция возвращает траты по заданной категории
    за последние три месяца (от переданной даты)."""

    logger.info("Запуск")

    if not date:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    three_month_ago = date - timedelta(days=92)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    filtered_data = transactions[
        (transactions["Дата операции"] >= three_month_ago)
        & (transactions["Дата операции"] <= date)
        & (transactions["Категория"] == category)
    ]

    return filtered_data
