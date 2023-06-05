from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.web.config import Config
    from aiohttp.web import Application


def setup_process_pool_executors(app: "Application"):
    """
    Устанавливает пул потоков для текущего экземпляра приложения.
    """
    config: "Config" = app["config"]
    executor = ThreadPoolExecutor(max_workers=config.app_config.max_workers)
    app["executor"] = executor
