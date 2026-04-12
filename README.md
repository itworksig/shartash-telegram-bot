# Shartash Telegram Bot

Telegram-бот на `aiogram 3`, который знакомит пользователя с проектом школы тропостроения и показывает информацию по кнопкам.

## Railway 部署

这个项目已经改成可直接部署到 Railway，并支持两种启动模式：

- `polling`：只需要 `BOT_TOKEN`，适合 Railway Worker 或本地运行。
- `webhook`：适合 Railway Web Service，会监听 `PORT`，并自动向 Telegram 注册 webhook。

如果你现在是在 Railway 普通服务里部署，建议直接用 `webhook` 模式，因为你已经配置了：

- `BOT_WEBHOOK_DOMAIN`
- `BOT_WEBHOOK_ENABLE`
- `BOT_WEBHOOK_PATH`
- `PORT`

### Railway 要填的命令

你截图里的 `npm run build` 和 `npm start` 是错的，这个项目是 Python，不是 Node.js。

把 Railway 里的命令改成下面这样：

`Pre-deploy Command`

```bash
poetry install --only main
```

`Custom Start Command`

```bash
poetry run shartash-bot
```

如果 Railway 环境里没有 `poetry`，也可以用：

```bash
python -m shartash_telegram_bot.main
```

但优先推荐：

```bash
poetry run shartash-bot
```

### Railway 必填环境变量

最少需要：

```env
BOT_TOKEN=你的_telegram_bot_token
```

如果使用 webhook 模式，再配置：

```env
BOT_WEBHOOK_ENABLE=true
BOT_WEBHOOK_DOMAIN=https://你的Railway域名
BOT_WEBHOOK_PATH=/webhook
PORT=8080
```

例如：

```env
BOT_TOKEN=1234567890:AAExampleRealTelegramToken
BOT_WEBHOOK_ENABLE=true
BOT_WEBHOOK_DOMAIN=https://your-app.up.railway.app
BOT_WEBHOOK_PATH=/webhook
PORT=8080
```

最终 webhook 地址会是：

```text
https://your-app.up.railway.app/webhook
```

### 你截图里的变量说明

- `BOT_TOKEN`：必须保留，这是 Telegram BotFather 给你的真实 token。
- `BOT_WEBHOOK_ENABLE`：如果填 `true`，程序会以 webhook 模式启动。
- `BOT_WEBHOOK_DOMAIN`：必须是 Railway 分配给你的公网 HTTPS 域名，比如 `https://xxx.up.railway.app`。
- `BOT_WEBHOOK_PATH`：可保留 `/webhook`。
- `PORT`：Railway 注入的端口，通常无需手动乱改，程序会读取。
- `BOT_STORE`、`REDIS_URL`、`TZ`、`NODE_ENV`：当前代码里并不依赖它们，不会影响启动。

### 本地启动命令

本地 `.env` 示例：

```env
BOT_TOKEN=你的_telegram_bot_token
BOT_WEBHOOK_ENABLE=false
```

启动：

```bash
poetry install
poetry run shartash-bot
```

## 1. Назначение проекта

Бот реализует простой сценарий диалога:

1. Пользователь отправляет `/start`.
2. Бот отправляет приветственный текст.
3. Бот показывает `ReplyKeyboard` (кнопки внизу чата).
4. При нажатии на кнопку бот отправляет соответствующий информационный блок.

Проект сделан в `src-layout` и запускается как Python-модуль.

## 2. Стек и зависимости

- Python `>=3.11,<3.15`
- Poetry (управление зависимостями и запуском)
- `aiogram >=3.26.0,<4.0.0`
- `python-dotenv >=1.2.2,<2.0.0`

Файл зависимостей: `pyproject.toml`.

## 3. Структура проекта

```text
.
├── pyproject.toml
├── poetry.lock
├── README.md
├── src/
│   └── shartash_telegram_bot/
│       ├── __init__.py
│       ├── main.py         # Точка входа: Bot + Dispatcher + polling
│       ├── handlers.py     # Обработчики сообщений и роутер
│       ├── keyboards.py    # Клавиатура (ReplyKeyboardMarkup)
│       └── content.py      # Текстовый контент (intro, разделы, модули)
└── tests/
```

## 4. Принцип работы программы (подробно)

### 4.1 Общая схема выполнения

1. При старте запускается `main.py`.
2. `load_dotenv()` подгружает переменные окружения из `.env`.
3. Из `BOT_TOKEN` создается объект `Bot`.
4. Создается `Dispatcher`.
5. Роутер из `handlers.py` подключается через `dp.include_router(router)`.
6. `dp.start_polling(bot)` начинает long polling:
   - бот периодически запрашивает новые update у Telegram API;
   - каждый входящий update проходит через роутер;
   - при совпадении фильтра вызывается соответствующий handler.

### 4.2 Как появляется клавиатура

Клавиатура объявляется в `keyboards.py` как `ReplyKeyboardMarkup`.

Она отображается только если передать ее в ответе:

```python
await message.answer(intro_text, reply_markup=main_keyboard)
```

Поэтому клавиатура отправляется в `start_handler` в `handlers.py`.

### 4.3 Как обрабатываются кнопки

В этом проекте кнопки работают как обычные текстовые сообщения.

Пример:

- Кнопка с текстом `О проекте`
- Пользователь нажимает кнопку
- Клиент Telegram отправляет текст `О проекте`
- Срабатывает handler с условием `lambda msg: msg.text == "О проекте"`

То есть маршрутизация построена на точном совпадении `message.text`.

### 4.4 Откуда берется контент

Все длинные тексты вынесены в `content.py`:

- `intro_text`
- `project_info`
- `grant_info`
- `modules` (словарь модулей)

Это разделяет логику (handlers) и данные (content), и упрощает поддержку.

## 5. Установка и запуск

### 5.1 Предварительные требования

1. Установить Python 3.11+.
2. Установить Poetry.
3. Создать бота через [@BotFather](https://t.me/BotFather) и получить токен.

### 5.2 Установка зависимостей

В корне проекта:

```bash
poetry install
```

### 5.3 Настройка `.env`

Создайте файл `.env` в корне:

```env
BOT_TOKEN=ваш_токен_бота
```

### 5.4 Команда запуска (текущий стандарт проекта)

```bash
poetry run shartash-bot
```

Альтернативно:

```bash
poetry run python -m shartash_telegram_bot.main
```

После старта в консоли будет:

```text
INFO:__main__:Starting bot in polling mode
```

## 6. Подробный разбор файлов: что и где менять

### `src/shartash_telegram_bot/main.py`

Изменяйте этот файл, если нужно:

- менять способ запуска (polling/webhook);
- добавлять глобальные middleware, логирование, обработку ошибок;
- подключать дополнительные роутеры.

Ключевые обязанности файла:

- загрузка env;
- создание `Bot` и `Dispatcher`;
- запуск event-loop/polling.

### `src/shartash_telegram_bot/handlers.py`

Изменяйте этот файл, если нужно:

- добавить новые команды/кнопки;
- изменить реакцию на сообщения;
- добавить фильтры или FSM-сценарии.

Здесь находится основная бизнес-логика обработки входящих сообщений.

### `src/shartash_telegram_bot/keyboards.py`

Изменяйте этот файл, если нужно:

- добавить/удалить кнопки;
- изменить расположение кнопок по строкам;
- включить дополнительные параметры клавиатуры.

Важно: после изменения клавиатуры нужно убедиться, что соответствующие handlers существуют.

### `src/shartash_telegram_bot/content.py`

Изменяйте этот файл, если нужно:

- обновить тексты;
- добавить новые тематические блоки;
- редактировать список учебных модулей.

Рекомендуется хранить весь пользовательский контент здесь, а не хардкодить в handlers.

### `.env`

Изменяйте этот файл, если нужно:

- заменить токен;
- добавить новые секреты (если проект расширится).

Никогда не публикуйте `.env` в публичный репозиторий.

### `pyproject.toml`

Изменяйте этот файл, если нужно:

- добавить зависимости;
- поменять ограничения Python;
- настроить упаковку/метаданные проекта.

## 7. Как добавить новую кнопку (практический алгоритм)

Пример: добавить кнопку `Контакты`.

1. В `keyboards.py` добавить `KeyboardButton(text="Контакты")`.
2. В `content.py` добавить текст, например `contacts_info`.
3. В `handlers.py`:
   - импортировать `contacts_info`;
   - добавить handler:

```python
@router.message(lambda msg: msg.text == "Контакты")
async def contacts_handler(message: Message):
    await message.answer(contacts_info)
```

4. Перезапустить бота.
5. Отправить `/start`, чтобы клиент получил обновленную клавиатуру.

## 8. Типовые проблемы и диагностика

### Проблема: бот запущен, но кнопок не видно

Проверить:

1. Пользователь отправил `/start`.
2. В `start_handler` передается `reply_markup=main_keyboard`.
3. Бот перезапущен после изменений.
4. В клиенте Telegram клавиатура не скрыта вручную.

### Проблема: нажатие кнопки ничего не делает

Проверить:

1. Текст кнопки точно совпадает с фильтром в handler.
2. Роутер подключен в `main.py` (`dp.include_router(router)`).
3. Нет исключений во время запуска/обработки.

### Проблема: ошибки токена (`Unauthorized`, `Token is invalid`)

Проверить:

1. Значение `BOT_TOKEN` в `.env`.
2. Нет лишних пробелов/кавычек.
3. Запущен именно нужный `.env` в текущей директории.

### Проблема: `ModuleNotFoundError` при запуске

Проверить, что запуск идет именно так:

```bash
poetry run shartash-bot
```

## 9. Идеи для дальнейшего развития

- Перейти с `lambda`-фильтров на `F.text == ...` для более читаемых фильтров aiogram.
- Добавить `/help` и `/about` команды.
- Добавить inline-кнопки (`InlineKeyboardMarkup`) для ссылок и действий.
- Добавить логирование (`logging`) вместо `print`.
- Добавить тесты на handlers и контент.
- Добавить Dockerfile и `.env.example`.

## 10. Краткая памятка по запуску

```bash
poetry install
printf "BOT_TOKEN=...\n" > .env
PYTHONPATH=src poetry run python -m shartash_telegram_bot.main
```

Остановить бота: `Ctrl + C`.
