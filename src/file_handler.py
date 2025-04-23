import pandas as pd


def xlsx_handler(path: str) -> pd.DataFrame:
    """Возвращает DataFrame"""

    return pd.read_excel(path).fillna(0.0)


def xlsx_handler_to_dict(path: str) -> list[dict]:
    """Преобразует DataFrame в словарь со структурой указанной в задании.
    Заменяет nan на 0 по всему DataFrame"""

    data_list = []
    df = pd.read_excel(path)
    df = df.fillna(0)

    for index, row in df.iterrows():
        data_list.append(
            {
                "date of operation": row["Дата операции"],
                "date of currency": row["Дата платежа"],
                "card number": row["Номер карты"],
                "status": row["Статус"],
                "operation": {"add": row["Сумма операции"], "currency": row["Валюта операции"]},
                "add": row["Сумма платежа"],
                "currency": row["Валюта платежа"],
                "cashback": row["Кэшбэк"],
                "category": row["Категория"],
                "description": row["Описание"],
                "Investment bank": row["Округление на инвесткопилку"],
                "add with round": row["Сумма операции с округлением"],
            }
        )

    return data_list
