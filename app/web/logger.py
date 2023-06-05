import logging
import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_logging(_: "Application") -> None:
    """
    Устанавливает logging.

    Args:
        _ (Application): Экземпляр класса Application.
    """
    logging.basicConfig(level=logging.ERROR)
