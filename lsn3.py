import asyncio
from initial import MyBot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()
buttons = ["btn1", "btn2", "btn3", "btn4"]

for but in buttons:
    builder.button(text=but)

builder.adjust(3)  # по 3 кнопки в ряд
keyboard = builder.as_markup(
    resize_keyboard=True,  # кнопки будут адаптироваться в размер экрана
    one_time_keyboard=False  # сворачивает клавиатуру после нажатия на любую из кнопок
)


class ExtendBot(MyBot):
    def __init__(self):
        super().__init__()

    def handlers(self):
        super().handlers()

        @self.dp.message(Command("menu"))
        async def cmd_test(message: Message):
            # отправка клавиатуры пользователю
            await message.answer(f"Меню:", reply_markup=keyboard)  # отправка кнопок reply_markup


if __name__ == '__main__':
    bot = ExtendBot()
    asyncio.run(bot.run_bot())
