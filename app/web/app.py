from aiohttp.web import Application
from aiohttp_apispec import setup_aiohttp_apispec
import aiohttp_cors

from app.store.database.config import setup_database
from app.web.config import setup_config
from app.web.logger import setup_logging
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes
from app.web.pool_executors import setup_process_pool_executors


def setup_cors(app: Application):
    """
    Устанавливает обработку CORS для приложения.

    Args:
        app (Application): Экземпляр приложения.
    """
    app["cors"] = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_headers='*',
        )
    })


def setup_app(config_path: str) -> Application:
    """
    Создает экземпляр приложения и устанавливает ключевые
    элементы приложения (loger, database, routes, middleware, cors, config).
    Метод вызывается один раз в момент старта приложения.

    Returns: Возвращает экземпляр приложения.
    """

    app = Application()
    setup_logging(app)
    setup_config(app, config_path)
    setup_cors(app)
    setup_aiohttp_apispec(app, static_path='/swagger_static',
                          title='mp3-converter', url='/docs/json',
                          swagger_path='/docs')
    setup_routes(app)
    setup_middlewares(app)
    setup_database(app)
    setup_process_pool_executors(app)
    return app
