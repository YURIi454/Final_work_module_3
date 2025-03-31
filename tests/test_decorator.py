import pandas as pd
from _pytest.capture import CaptureFixture

from config import ROOT_DIR
from src.decorator import log


def test_log() -> None:
    """Тестирование декоратора."""

    @log("decorator_test")
    def write_file() -> pd.DataFrame:
        return pd.DataFrame([{"test": "deco"}])

    write_file()
    with open(ROOT_DIR + "/logs/log_test.log", mode="r", encoding="utf-8") as file:
        log_rear = file.read()
    assert "" in log_rear


def test_log_cons(capsys: CaptureFixture) -> None:
    """Тест декоратора."""

    @log()
    def write_cons() -> pd.DataFrame:
        return pd.DataFrame([{"test": "deco"}])

    write_cons()
    check_out = capsys.readouterr()
    assert "" in check_out.out
