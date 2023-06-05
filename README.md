# MP3 converter.
Тест задание от компании Bewise https://bewise.ai/ на должность junior python developer.

## Стэк технологий:
 - python
 - aiohttp
 - Postgresql

## Тест задание:
Необходимо реализовать веб-сервис, выполняющий следующие функции:
1. Создание пользователя;
2. Для каждого пользователя - сохранение аудиозаписи в формате wav, преобразование её в формат mp3 и запись в базу данных и предоставление ссылки для скачивания аудиозаписи.

### Детализация задачи:
1. С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - PostgreSQL). Предоставить все необходимые скрипты и конфигурационные (docker/compose) файлы для развертывания СУБД, а также инструкции для подключения к ней. Необходимо обеспечить сохранность данных при рестарте контейнера, то есть - использовать volume-ы для хранения файлов СУБД на хост-машине.
2. Реализовать веб-сервис со следующими REST методами:
   1. Создание пользователя, POST:
      1. Принимает на вход запросы с именем пользователя;
      2. Создаёт в базе данных пользователя заданным именем, так же генерирует уникальный идентификатор пользователя и UUID токен доступа (в виде строки) для данного пользователя;
      3. Возвращает сгенерированные идентификатор пользователя и токен.
   2. Добавление аудиозаписи, POST:
      1. Принимает на вход запросы, содержащие уникальный идентификатор пользователя, токен доступа и аудиозапись в формате wav;
      2. Преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет их в базе данных;
      3. Возвращает URL для скачивания записи вида http://host:port/record?id=id_записи&user=id_пользователя.
   3. Доступ к аудиозаписи, GET:
      1. Предоставляет возможность скачать аудиозапись по ссылке из п 2.2.3.
3. Для всех сервисов метода должна быть предусмотрена обработка различных ошибок, возникающих при выполнении запроса, с возвращением соответствующего HTTP статуса.
4. Модель данных (таблицы, поля) для каждого из заданий можно выбрать по своему усмотрению.
5. В репозитории с заданием должны быть предоставлены инструкции по сборке докер-образа с сервисами из пп. 2. и 3., их настройке и запуску. А также пример запросов к методам сервиса.
6. Желательно, если при выполнении задания вы будете использовать docker-compose, SQLAlchemy, пользоваться аннотацией типов.

## Запуск:
0. Для работы веб-сервиса необходимо установить приложение FFmpeg https://ffmpeg.org/

1. Клонировать репозиторий.

2. Зайти в директорию проекта.
```
cd mp3_converter/
```

3. Создать .venv в директории mp3_converter.
```
python3 -m venv .venv
```

4. Активировать виртуальную среду.
```
source .venv/bin/activate
```
5. Установить зависимости.
```
pip install -r requirements.txt
```

6. Установить разрешение на выполнение файла run.sh.
```
chmod +x run.sh
```

7. Создать бд.
```
make compose-up
```

8. Применить миграции.
```
make migrate-up
```

9. Запустить приложение.
```
./run.sh app
```

## Веб-сервис имеет следующие конечные точки:

### 1. /users.create
POST-запрос для создания нового пользователя.

### Пример запроса:
```
curl -X 'POST' \
  'http://127.0.0.1:8080/users.create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "string"
}'
```

### Пример ответа:
```
{
  "status": "ok",
  "data": {
    "uuid": "6f3ea70f-73b9-4e8a-9524-f676fb8794f7",
    "username": "string",
    "id": 5
  }
}
```

### 2. /files.convert
POST-запрос для конвертации файла из формата WAV в формат mp3.
Примеры отправляемых файлов на веб-сервис для конвертации в формат mp3 лежат в директории audio/.

### Пример успешного запроса:
```
curl --location 'http://127.0.0.1:8080/files.convert' \
--header 'user_id: 5' \
--header 'user_uuid: 6f3ea70f-73b9-4e8a-9524-f676fb8794f7' \
--form 'filename=@"audio/file_example_WAV_10MG.wav"'
```
### Пример ответа:
```
{
    "status": "ok",
    "url": "http://0.0.0.0:8080/files.record?record_id=4&user_id=5"
}
```

### Пример неуспешного запроса (отправляем файл с некорректным содержанием данных):
```
curl --location 'http://127.0.0.1:8080/files.convert' \
--header 'user_id: 5' \
--header 'user_uuid: 6f3ea70f-73b9-4e8a-9524-f676fb8794f7' \
--form 'filename=@"audio/incorrect_file.txt"'
```

### Пример ответа:
```
{
    "code": 400,
    "status": "bad_request",
    "message": "Invalid file. Failed to convert file to mp3 format.",
    "data": {}
}
```

### 2. /files.record?record_id=4&user_id=5"
Get-запрос для скачивания конвертированного файла в формате mp3.

### Пример запроса.
Файл будет скачан в директорию из которой Вы вызываете команды в терминале.

```
curl --location 'http://127.0.0.1:8080/files.record?record_id=4&user_id=5' --output out.mp3
```

В случае если пользователь или файл не был найден, ответ будет следующим:
```
{"code": 404, "status": "not found", "message": "User or required mp3 file not found", "data": {}}
```