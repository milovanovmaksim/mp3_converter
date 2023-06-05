from typing import TYPE_CHECKING

from app.users.routes import setup_routes as user_setup_routes
from app.mp3_files.routes import setup_routes as file_setup_routes


if TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    """
    Устанавливает конечные точки веб-приложения.

    Args:
        app (Application): _description_
    """
    user_setup_routes(app)
    file_setup_routes(app)
