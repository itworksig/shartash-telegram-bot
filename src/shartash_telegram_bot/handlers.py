from aiogram import Router
from aiogram.types import Message
from shartash_telegram_bot.content import intro_text, project_info, grant_info, modules
from shartash_telegram_bot.keyboards import main_keyboard

router = Router()


@router.message(lambda msg: msg.text == "/start")
async def start_handler(message: Message):
    await message.answer(intro_text, reply_markup=main_keyboard)


@router.message(lambda msg: msg.text == "О проекте")
async def project_handler(message: Message):
    await message.answer(project_info)


@router.message(lambda msg: msg.text == "О гранте")
async def grant_handler(message: Message):
    await message.answer(grant_info)


@router.message(lambda msg: msg.text == "Учебные модули")
async def modules_handler(message: Message):
    text = "\n".join(modules.values())
    await message.answer(text)


@router.message(lambda msg: msg.text == "О клубе")
async def club_handler(message: Message):
    await message.answer(
        "Подробнее о клубе: https://vk.com/shartash_frends_club"
    )
