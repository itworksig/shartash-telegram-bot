import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import ErrorEvent, Message
from shartash_telegram_bot.content import intro_text, project_info, grant_info, modules
from shartash_telegram_bot.keyboards import main_keyboard

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_handler(message: Message):
    logger.info("Handling /start for chat_id=%s", message.chat.id)
    await message.answer(intro_text, reply_markup=main_keyboard)


@router.message(F.text == "О проекте")
async def project_handler(message: Message):
    logger.info("Handling 'О проекте' for chat_id=%s", message.chat.id)
    await message.answer(project_info)


@router.message(F.text == "О гранте")
async def grant_handler(message: Message):
    logger.info("Handling 'О гранте' for chat_id=%s", message.chat.id)
    await message.answer(grant_info)


@router.message(F.text == "Учебные модули")
async def modules_handler(message: Message):
    logger.info("Handling 'Учебные модули' for chat_id=%s", message.chat.id)
    text = "\n".join(modules.values())
    await message.answer(text)


@router.message(F.text == "О клубе")
async def club_handler(message: Message):
    logger.info("Handling 'О клубе' for chat_id=%s", message.chat.id)
    await message.answer(
        "Подробнее о клубе: https://vk.com/shartash_frends_club"
    )


@router.message()
async def unknown_message_handler(message: Message):
    logger.info(
        "Handling fallback message text=%r chat_id=%s",
        message.text,
        message.chat.id,
    )
    await message.answer(
        "Пожалуйста, используйте кнопки ниже или отправьте /start."
    )


@router.errors()
async def error_handler(event: ErrorEvent):
    logger.exception("Unhandled bot error: %s", event.exception)
    return True
