import asyncio
from aiogram.filters import Command  # фильтрация команд
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from initial import MyBot

# кнопки вообще можно объявлять и в других файлах
BTN1 = KeyboardButton(text="btn1")  # создаём саму кнопку и к ней добавляем название
BTN2 = KeyboardButton(text="btn2")
HIDE_MENU = KeyboardButton(text="hide_menu")

# формируем сет из кнопок (собственно говоря само меню)
MENU = ReplyKeyboardMarkup(
    keyboard=[
        [BTN1, BTN2],  # 1 ряд из кнопок
        [HIDE_MENU, ],
    ],
    resize_keyboard=True  # клавиатура адаптируется под размер экрана
)


class ExtendBot(MyBot):

    def __init__(self):
        super().__init__()

    def handlers(self):
        super().handlers()

        # 1. отдаём пользователю меню
        @self.dp.message(Command("menu"))
        async def cmd_test(message: Message):
            # отправка клавиатуры пользователю
            await message.answer(f"Меню:", reply_markup=MENU)  # отправка кнопок reply_markup

        # 2. добавляем обработчики нажатий кнопок меню
        # ВНИМАНИЕ В КАЧЕСТВЕ ОБРАБОТЧИКОВ ЗДЕСЬ ИСПОЛЬЗУЕТСЯ message.text А НЕ Command, кнопка это текст
        @self.dp.message(lambda message: message.text == "btn1")
        async def cmd_btn1(message: Message):
            # обработчик нажатия btn1 (собственно кнопка это по сути тот же текст отправленный пользователем (команда)
            await message.answer(f"Нажата кнопка btn1")

        @self.dp.message(lambda message: message.text == "btn2")
        async def cmd_btn2(message: Message):
            # обработчик нажатия btn2 (собственно кнопка это по сути тот же текст отправленный пользователем (команда)
            await message.answer(f"Нажата кнопка btn2")

        # 3. сокрытие клавиатуры если требуется
        @self.dp.message(lambda message: message.text == "hide_menu")
        async def cmd_hide_menu(message: Message):
            # просто убираем клавиатуру ReplyKeyboardRemove()
            await message.answer("Клавиатура скрыта", reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    try:
        my_bot = ExtendBot()
        asyncio.run(my_bot.run_bot())
    except Exception as err:
        print(err)
