from dataclasses import dataclass
from aiohttp.web import Application

import yaml

from app.store.database.database import Database


@dataclass
class DatabaseConfig:
    """
    Класс, содержащий конфигурационные настройки базы данных.
    """
    host: str
    port: int
    user: str
    password: str
    database: str


def setup_config(config_path: str) -> DatabaseConfig:
    """
    Устанавливает конфигурационные настройки базы даннах.
    Args:
        config_path (str): Путь к конфигурационному файлу.
    Returns: Возвращает экземпляр класса DatabaseConfig.
    """
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    return DatabaseConfig(**raw_config["database"])


def setup_database(app: "Application"):
    """
    Устанавливает экземпляр класса Database для текущего экземпляра приложения Application.
    Также, добавляет методы Database.connect и Database.disconnect в сигналы.

    Args:
        app (Application): _description_
    """
    config: DatabaseConfig = app["config"].database
    app["database"] = Database(config)
    app.on_startup.append(app["database"].connect)
    app.on_cleanup.append(app["database"].disconnect)
