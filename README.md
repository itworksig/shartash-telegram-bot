# Shartash Telegram Bot

Телеграм-бот на `aiogram 3`, который отвечает на команду `/start`, показывает клавиатуру и отправляет пользователю информационные блоки о проекте, гранте, учебных модулях и клубе.

## Что умеет бот

- отвечает на `/start`;
- показывает `ReplyKeyboard` с основными разделами;
- отправляет тексты по кнопкам:
  - `О проекте`
  - `О гранте`
  - `Учебные модули`
  - `О клубе`

## Стек

- Python `>=3.11,<3.15`
- `aiogram >=3.26.0,<4.0.0`
- `python-dotenv >=1.2.2,<2.0.0`
- Poetry

## Структура проекта

```text
.
├── main.py
├── pyproject.toml
├── poetry.lock
├── README.md
├── src/
│   └── shartash_telegram_bot/
│       ├── __init__.py
│       ├── content.py
│       ├── handlers.py
│       ├── keyboards.py
│       └── main.py
└── tests/
```

## Как запустить локально

### 1. Установить зависимости

```bash
poetry install
```

### 2. Создать `.env`

В корне проекта создайте файл `.env`:

```env
BOT_TOKEN=ваш_токен_бота
BOT_WEBHOOK_ENABLE=false
```

### 3. Запустить бота

Основная команда:

```bash
poetry run python main.py
```

Альтернативная команда:

```bash
poetry run shartash-bot
```

После запуска в логах должно появиться:

```text
INFO:shartash_telegram_bot.main:Starting bot in polling mode
INFO:aiogram.dispatcher:Start polling
```

После этого можно открыть Telegram и отправить боту команду `/start`.

## Как работает запуск

Проект поддерживает два режима:

- `polling`:
  - используется по умолчанию;
  - подходит для локального запуска и для worker-сервисов;
  - достаточно переменной `BOT_TOKEN`.
- `webhook`:
  - включается, если `BOT_WEBHOOK_ENABLE=true`;
  - подходит для Railway web service;
  - приложение поднимает HTTP-сервер на порту из `PORT`;
  - webhook автоматически регистрируется в Telegram.

## Переменные окружения

### Обязательные

```env
BOT_TOKEN=ваш_токен_бота
```

### Для webhook-режима

```env
BOT_WEBHOOK_ENABLE=true
BOT_WEBHOOK_DOMAIN=https://your-app.up.railway.app
BOT_WEBHOOK_PATH=/webhook
PORT=8080
```

Описание:

- `BOT_TOKEN`: токен бота из `@BotFather`.
- `BOT_WEBHOOK_ENABLE`: если `true`, бот запускается в webhook-режиме.
- `BOT_WEBHOOK_DOMAIN`: публичный HTTPS-домен сервиса.
- `BOT_WEBHOOK_PATH`: путь webhook. Если не указан, используется `/webhook`.
- `PORT`: порт, который выделяет Railway. Обычно подставляется автоматически.

## Деплой на Railway

Этот проект подготовлен для Railway. Если сервис создается как обычный web service, рекомендуется использовать webhook-режим.

### Что указать в Railway

`Pre-deploy Command`

```bash
poetry install --only main
```

`Custom Start Command`

```bash
poetry run python main.py
```

### Какие переменные добавить

Минимальный набор для Railway:

```env
BOT_TOKEN=ваш_реальный_telegram_token
BOT_WEBHOOK_ENABLE=true
BOT_WEBHOOK_DOMAIN=https://your-app.up.railway.app
BOT_WEBHOOK_PATH=/webhook
```

Итоговый webhook будет таким:

```text
https://your-app.up.railway.app/webhook
```

### Что не нужно указывать

Для этого проекта не нужны Node.js-команды вроде:

```bash
npm run build
npm start
```

Это Python-проект, поэтому запуск должен идти через `poetry` или `python`.

## Как изменить тексты и кнопки

### Тексты

Файл:

[src/shartash_telegram_bot/content.py](/Users/yxxiao/Documents/GitHub/New/shartash-telegram-bot/src/shartash_telegram_bot/content.py)

Здесь находятся:

- `intro_text`
- `project_info`
- `grant_info`
- `modules`

### Кнопки

Файл:

[src/shartash_telegram_bot/keyboards.py](/Users/yxxiao/Documents/GitHub/New/shartash-telegram-bot/src/shartash_telegram_bot/keyboards.py)

Здесь задается `ReplyKeyboardMarkup`.

### Логика обработки

Файл:

[src/shartash_telegram_bot/handlers.py](/Users/yxxiao/Documents/GitHub/New/shartash-telegram-bot/src/shartash_telegram_bot/handlers.py)

Здесь находятся обработчики сообщений и маршрутизация по тексту кнопок.

### Точка входа

Файл:

[main.py](/Users/yxxiao/Documents/GitHub/New/shartash-telegram-bot/main.py)

Это совместимый стартовый файл для Railway и других окружений, где `src/` не добавляется в `PYTHONPATH` автоматически.

Файл:

[src/shartash_telegram_bot/main.py](/Users/yxxiao/Documents/GitHub/New/shartash-telegram-bot/src/shartash_telegram_bot/main.py)

Здесь происходит:

- выбор и запуск совместимого корневого entrypoint;
- загрузка переменных окружения;
- выбор режима `polling` или `webhook`;
- запуск `Dispatcher`;
- регистрация webhook при необходимости.

## Как добавить новую кнопку

Пример: нужно добавить кнопку `Контакты`.

1. В [src/shartash_telegram_bot/keyboards.py](/Users/yxxiao/Documents/GitHub/New/shartash-telegram-bot/src/shartash_telegram_bot/keyboards.py) добавить кнопку:

```python
KeyboardButton(text="Контакты")
```

2. В [src/shartash_telegram_bot/content.py](/Users/yxxiao/Documents/GitHub/New/shartash-telegram-bot/src/shartash_telegram_bot/content.py) добавить текст:

```python
contacts_info = "Текст раздела Контакты"
```

3. В [src/shartash_telegram_bot/handlers.py](/Users/yxxiao/Documents/GitHub/New/shartash-telegram-bot/src/shartash_telegram_bot/handlers.py) добавить обработчик:

```python
@router.message(lambda msg: msg.text == "Контакты")
async def contacts_handler(message: Message):
    await message.answer(contacts_info)
```

4. Перезапустить бота.

## Типовые проблемы

### Бот не запускается

Проверьте:

- задан ли `BOT_TOKEN`;
- установлен ли Poetry;
- выполнена ли команда `poetry install`.
- для Railway и других окружений без `PYTHONPATH=src` используйте `poetry run python main.py`.

### Ошибка `Token is invalid` или `Unauthorized`

Проверьте:

- актуален ли токен из `@BotFather`;
- нет ли лишних пробелов или кавычек;
- не был ли токен перевыпущен.

### В Railway сервис поднялся, но бот не отвечает

Проверьте:

- `BOT_WEBHOOK_ENABLE=true`;
- `BOT_WEBHOOK_DOMAIN` указывает на реальный Railway-домен;
- путь `BOT_WEBHOOK_PATH` совпадает с тем, который использует приложение;
- сервис действительно доступен по HTTPS.

### Кнопки не появляются

Проверьте:

- пользователь отправил `/start`;
- клавиатура передается через `reply_markup=main_keyboard`;
- бот был перезапущен после изменений.

## Команды запуска

Локально:

```bash
poetry run python main.py
```

Railway:

```bash
poetry install --only main
poetry run python main.py
```
