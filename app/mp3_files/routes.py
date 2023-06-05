from typing import TYPE_CHECKING


from app.mp3_files.views import ConvertFileView, DownloadMp3FileView

if TYPE_CHECKING:
    from aiohttp.web import Application
    from aiohttp_cors import CorsConfig


def setup_routes(app: "Application"):
    """
    Устанавливает конечные точки для манипуляции данными в таблице "mp3_files" базы данных.
    """
    cors: "CorsConfig" = app["cors"]
    cors.add(app.router.add_view("/files.convert", ConvertFileView))
    cors.add(app.router.add_view("/files.record", DownloadMp3FileView))
