from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="О проекте")],
        [KeyboardButton(text="О гранте")],
        [KeyboardButton(text="Учебные модули")],
        [KeyboardButton(text="О клубе")]
    ],
    resize_keyboard=True
)