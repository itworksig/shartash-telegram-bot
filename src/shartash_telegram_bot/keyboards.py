from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Основная клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="О проекте")],
        [KeyboardButton(text="О гранте")],
        [KeyboardButton(text="Учебные модули")],
        [KeyboardButton(text="О клубе")],
        [KeyboardButton(text="О тропостроении")],
        [KeyboardButton(text="Построенные объекты")],
        [KeyboardButton(text="🏠 Главное меню")]
    ],
    resize_keyboard=True
)

# Клавиатура подменю "О тропостроении"
tropostroyenie_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Общая информация о тропостроении")],
        [KeyboardButton(text="🎥 Интервью о тропостроении")],
        [KeyboardButton(text="🎓 Вводная лекция школы")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

# Клавиатура подменю "Построенные объекты"
objects_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏛️ Археологическая беседка")],
        [KeyboardButton(text="🏖️ Южный берег друзей Шарташа")],
        [KeyboardButton(text="🚪 Входная группа тропы здоровья")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)