import asyncio
from aiogram.filters import Command
from aiogram.types import Message
from initial import MyBot

"""
Добавление обработчиков команд (формата "/start") в telegram
"""


class ExtendBot(MyBot):
    def __init__(self):
        super().__init__()  # расширение класса бота

    def handlers(self):
        super().handlers()  # расширение базовой функции

        @self.dp.message(Command("test"))
        async def cmd_test(message: Message):
            await message.answer(f"{message.text} Запущена команда test")


if __name__ == '__main__':
    try:
        my_bot = ExtendBot()
        asyncio.run(my_bot.run_bot())
    except Exception as err:
        print(err)
