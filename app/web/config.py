from typing import Any, TYPE_CHECKING
from dataclasses import dataclass
import multiprocessing

import yaml

from app.store.database.config import setup_config as setup_db_config

if TYPE_CHECKING:
    from app.web.app import Application
    from app.store.database.config import DatabaseConfig


@dataclass
class AppConfig:
    """
    Класс, содержащий общие настройки веб-приложения.
    Args:
        host: Хост.
        port: Порт.
        base_url: Базовый url адрес веб-приложения.
        max_workers: Количество CPUs.
    """
    host: str
    port: int
    base_url: str
    max_workers: int


def setup_app_config(config_path: str) -> AppConfig:
    with open(config_path, "r") as f:
        raw_config: dict[Any, Any] = yaml.safe_load(f)
    max_workers = multiprocessing.cpu_count()
    raw_config["application"].update({"max_workers": max_workers})
    return AppConfig(**raw_config["application"])


@dataclass
class Config:
    """
    Класс, содержащий настройки ключевых элементов приложения.
    """
    database: "DatabaseConfig"
    app_config: "AppConfig"


def setup_config(app: "Application", config_path: str):
    """
    Конфигурирует приложения.

    Args:
        app (Application): Экземпляр класса Application
        config_path (str): Путь к конфигурационному файлу.
    """
    database_config = setup_db_config(config_path)
    app_config = setup_app_config(config_path)
    app["config"] = Config(database=database_config, app_config=app_config)
