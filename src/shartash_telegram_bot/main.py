import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

from shartash_telegram_bot.handlers import router

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is required")
    return value


def is_truthy(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def normalize_webhook_path(path: str | None) -> str:
    if not path:
        return "/webhook"
    return path if path.startswith("/") else f"/{path}"


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(router)
    return dp


async def run_polling() -> None:
    token = require_env("BOT_TOKEN")
    bot = Bot(token=token)
    dp = build_dispatcher()

    logger.info("Starting bot in polling mode")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def run_webhook() -> None:
    token = require_env("BOT_TOKEN")
    domain = require_env("BOT_WEBHOOK_DOMAIN").rstrip("/")
    path = normalize_webhook_path(os.getenv("BOT_WEBHOOK_PATH"))
    port = int(os.getenv("PORT", "8080"))

    bot = Bot(token=token)
    dp = build_dispatcher()
    app = web.Application()
    webhook_url = f"{domain}{path}"

    @web.middleware
    async def request_logging_middleware(request: web.Request, handler):
        logger.info("Incoming HTTP %s %s", request.method, request.path)
        try:
            response = await handler(request)
            logger.info(
                "Completed HTTP %s %s with status=%s",
                request.method,
                request.path,
                response.status,
            )
            return response
        except Exception:
            logger.exception(
                "Unhandled HTTP exception for %s %s",
                request.method,
                request.path,
            )
            raise

    app.middlewares.append(request_logging_middleware)

    async def on_startup(bot: Bot) -> None:
        logger.info("Setting Telegram webhook to %s", webhook_url)
        await bot.set_webhook(webhook_url)

    async def on_shutdown(bot: Bot) -> None:
        logger.info("Deleting Telegram webhook")
        await bot.delete_webhook()
        await bot.session.close()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=path)
    setup_application(app, dp, bot=bot)

    logger.info("Starting bot in webhook mode on 0.0.0.0:%s%s", port, path)
    web.run_app(app, host="0.0.0.0", port=port)


def run() -> None:
    if is_truthy(os.getenv("BOT_WEBHOOK_ENABLE")):
        run_webhook()
        return

    asyncio.run(run_polling())


if __name__ == "__main__":
    run()
