import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import ErrorEvent, Message
from shartash_telegram_bot.content import (
    intro_text,
    project_info,
    grant_info,
    modules,
    tropostroyenie_info,
    tropostroyenie_video_desc,
    tropostroyenie_lecture_desc,
    objects_info,
    archeological_gazebo,
    southern_coast,
    entrance_group,
    club_info,
)
from shartash_telegram_bot.keyboards import (
    main_keyboard,
    tropostroyenie_keyboard,
    objects_keyboard,
)

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
    await message.answer(club_info)


@router.message(F.text == "О тропостроении")
async def tropostroyenie_menu_handler(message: Message):
    logger.info("Handling 'О тропостроении' for chat_id=%s", message.chat.id)
    await message.answer(
        "Выберите раздел о тропостроении:",
        reply_markup=tropostroyenie_keyboard
    )


@router.message(F.text == "📖 Общая информация о тропостроении")
async def tropostroyenie_info_handler(message: Message):
    logger.info("Handling '📖 Общая информация о тропостроении' for chat_id=%s", message.chat.id)
    await message.answer(tropostroyenie_info)


@router.message(F.text == "🎥 Интервью о тропостроении")
async def tropostroyenie_video_handler(message: Message):
    logger.info("Handling '🎥 Интервью о тропостроении' for chat_id=%s", message.chat.id)
    await message.answer(tropostroyenie_video_desc)


@router.message(F.text == "🎓 Вводная лекция школы")
async def tropostroyenie_lecture_handler(message: Message):
    logger.info("Handling '🎓 Вводная лекция школы' for chat_id=%s", message.chat.id)
    await message.answer(tropostroyenie_lecture_desc)


@router.message(F.text == "Построенные объекты")
async def objects_menu_handler(message: Message):
    logger.info("Handling 'Построенные объекты' for chat_id=%s", message.chat.id)
    await message.answer(
        "Выберите объект для просмотра:",
        reply_markup=objects_keyboard
    )


@router.message(F.text == "🏛️ Археологическая беседка")
async def archeological_gazebo_handler(message: Message):
    logger.info("Handling '🏛️ Археологическая беседка' for chat_id=%s", message.chat.id)
    await message.answer(archeological_gazebo)


@router.message(F.text == "🏖️ Южный берег друзей Шарташа")
async def southern_coast_handler(message: Message):
    logger.info("Handling '🏖️ Южный берег друзей Шарташа' for chat_id=%s", message.chat.id)
    await message.answer(southern_coast)


@router.message(F.text == "🚪 Входная группа тропы здоровья")
async def entrance_group_handler(message: Message):
    logger.info("Handling '🚪 Входная группа тропы здоровья' for chat_id=%s", message.chat.id)
    await message.answer(entrance_group)


@router.message(F.text == "⬅️ Назад")
async def back_handler(message: Message):
    logger.info("Handling '⬅️ Назад' for chat_id=%s", message.chat.id)
    # Определяем, из какого подменю пришел пользователь,
    # и возвращаем соответствующее меню
    await message.answer(
        "Возвращаемся в главное меню:",
        reply_markup=main_keyboard
    )


@router.message(F.text == "🏠 Главное меню")
async def main_menu_handler(message: Message):
    logger.info("Handling '🏠 Главное меню' for chat_id=%s", message.chat.id)
    await message.answer(
        "Главное меню:",
        reply_markup=main_keyboard
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
