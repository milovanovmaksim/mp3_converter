from typing import TYPE_CHECKING

from app.users.views import UserCreteView

if TYPE_CHECKING:
    from aiohttp.web import Application
    from aiohttp_cors import CorsConfig


def setup_routes(app: "Application"):
    """
    Устанавливает конечные точки для манипуляции данными в таблице "users" базы данных.
    """
    cors: "CorsConfig" = app["cors"]
    cors.add(app.router.add_view("/users.create", UserCreteView))