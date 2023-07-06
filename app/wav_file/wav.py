import asyncio
from os import devnull, path
from datetime import datetime
from subprocess import Popen, PIPE
from typing import Optional, Tuple, Union, AsyncGenerator, TYPE_CHECKING
from tempfile import NamedTemporaryFile
import aiofiles.os

from aiohttp.web_exceptions import HTTPBadRequest
from app.store.database.database import Database

from app.mp3_files.models import Mp3FileModel


if TYPE_CHECKING:
    from aiohttp import BodyPartReader, MultipartReader
    from tempfile import _TemporaryFileWrapper
    from app.web.config import Config
    from concurrent.futures import ThreadPoolExecutor
    from aiohttp.web import Application


class WavFile:
    """
    Класс WavFile, представляющий файл формата WAV.

    Args:
        filename: Имя файла, полученного от пользователя.
        app: Экземпляр класса aiohttp.web.Application
        user_id: Идентификатор пользователя в базе данных.
    """

    def __init__(self, filename: str, app: "Application", user_id: int, *args, **kwargs):
        self.filename = filename
        self.user_id = user_id
        self.app = app
        self.database: Database = self.app["database"]
        self._loop = asyncio.get_event_loop()

    async def run(self, reader: Optional[Union["MultipartReader", "BodyPartReader"]]) -> str:
        """
        Запускает конвертацию файлов из формата WAV в формат mp3 на исполнение.

        Returns:
            Возвращает url адрес для скачивания mp3 файла.
        """

        in_temp_file = NamedTemporaryFile(mode="ab")
        async for chunk in self._read_by_chunck(reader):
            in_temp_file.write(chunk)

        out_path_file = await self._create_out_filepath()
        thread_pool_executor: "ThreadPoolExecutor" = self.app['executor']
        code, _, _ = await self._loop.run_in_executor(thread_pool_executor,
                                                      self._convert_to_mp3, in_temp_file, out_path_file)
        if code != 0:
            in_temp_file.close()
            raise HTTPBadRequest(reason="Invalid file. Failed to convert file to mp3 format.")
        mp3_file_model = await Mp3FileModel.inser_file(self.database, self.user_id, out_path_file, self.filename)
        url = self._generate_response(mp3_file_model.id)
        in_temp_file.close()
        return url

    async def _read_by_chunck(self, reader: Optional[Union["MultipartReader", "BodyPartReader"]]) -> AsyncGenerator:
        """
        Читает файл частями по 5 Мб из сокета, чтобы не хранить большие
        файлы в оперативной памяти. Файлы в формате WAV могут достигать до 4 Гб.
        chunck - прочитанные байты из сокета.
        """

        while True:
            chunk = await reader.read_chunk(5*1024*1024)  # type: ignore
            if not chunk:
                break
            yield chunk

    def _convert_to_mp3(self, temp: "_TemporaryFileWrapper", out_file) -> Tuple[int, bytes, bytes]:
        """ Конвертирует файл из формата WAV в формат mp3.
        Метод блокирующий, поэтому будем передавать его в пул потоков, чтобы не блокировать событийный цикл.

        Args:
            temp (_TemporaryFileWrapper):  Файлоподобный объект, используемый в качестве временного хранилища.
            Содержит данные, прочитанные из сокета. Имя файла temp.name перадется в программу ffmpeg https://ffmpeg.org/
            для конвертации в формат mp3.

        Returns:
            Tuple[code: int, stdout: bytes, stderr: bytes]:
                code - код состояния 0 или 1.
                code = 0 - операция завершена успешно.
                code = 1 - операция завершена с ошибкой.
                stdout - Стандартный поток вывода данных.
                stderr - Стандартный вывод ошибок.
        """

        ffmpeg = ["ffmpeg", "-y", "-i", temp.name, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", out_file]
        with open(devnull, 'rb') as dev_null:
            p = Popen(ffmpeg, stdin=dev_null, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        code = p.returncode
        temp.close()
        return code, stdout, stderr

    async def _create_directory(self) -> str:
        """
        Создает директорию в которую будет сохранен конвертированный файл.
        """

        current_date = datetime.now()
        current_date_string = current_date.strftime("%Y/%b/%d/%H/%M/%S")
        directory = path.join("./media", current_date_string)
        await aiofiles.os.makedirs(directory, exist_ok=True)
        return directory

    async def _create_out_filepath(self):
        """
        Создает путь для конвертированного файла.
        """

        directoty = await self._create_directory()
        out_file = path.join(directoty, self.filename + ".mp3")
        return out_file

    def _generate_response(self, file_id) -> str:
        """
        Создает url адрес для скачивания файла.
        """
        config: "Config" = self.app["config"]
        port = config.app_config.port
        base_url = config.app_config.base_url
        url = f"{base_url}:{port}/files.record?record_id={file_id}&user_id={self.user_id}"
        return url
