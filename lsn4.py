import asyncio
from initial import MyBot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery

"""
основная суть в том, что inline кнопки позволяют не отправлять текст, а именно нажимать на эту кнопку 
(за которой закреплен тот же самый текс в виде callback даты) и при нажатии на эту кнопку его ловит обработчик 
который имеет слой для работы с callback сигналами.
Но в основе лежит тот же текст, что и у кнопок типа ReplyKeyboardMarkup
"""


class ExtendBot(MyBot):
    def __init__(self):
        super().__init__()

    def handlers(self):
        super().handlers()

        @self.dp.message(Command("menu"))
        async def cmd_test(message: Message):
            # отправка клавиатуры пользователю
            keyboard = self.create_inline_keyboard()
            await message.answer(f"Меню:", reply_markup=keyboard)  # отправка кнопок reply_markup

        @self.dp.callback_query(lambda c: c.data and c.data.startswith("btn_"))
        async def process_callback(callback: CallbackQuery):
            await callback.answer()
            btn_id = callback.data  # получение callback даты закрепленной за кнопкой и ветвление действий
            if btn_id == "btn_1":
                await callback.message.answer(f"Нажата btn_1")
            elif btn_id == "btn_2":
                await callback.message.answer(f"Нажата btn_2")

    # создание inline клавиатуры, (кнопки которые появляются в чате, и несут уже в себе текст callback_data)
    @staticmethod
    def create_inline_keyboard():
        builder = InlineKeyboardBuilder()

        builder.button(text="btn 1", callback_data='btn_1')
        builder.button(text="btn 2", callback_data='btn_2')
        builder.adjust(1)
        return builder.as_markup()


if __name__ == '__main__':
    bot = ExtendBot()
    asyncio.run(bot.run_bot())
