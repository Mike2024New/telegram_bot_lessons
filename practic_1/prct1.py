import asyncio
from initial import MyBot
from aiogram.filters import Command
from aiogram.types import Message
from utilits.WORK_JSON import rec_json, read_json

"""
список пользователей (для практики здесь хранилищем будет простой json)
но такое решение подходит только для простых случаев, для продакшн использ postgres например
ВНИМАНИЕ! НАПОМНЮ ЕЩЁ РАЗ, ЧТО ДЛЯ ПРОДАКШН И БОЛЬШОГО КОЛИЧЕСТВА ПОЛЬЗОВАТЕЛЕЙ СПОСОБ РЕАЛИЗАЦИИ ЧЕРЕЗ JSON НЕ ПОДОЙДЕТ
В ДАЛЬШЕЙШЕМ ЭТОТ ВАРИАНТ БУДЕТ ПРОРАБОТАН НА POSTGRES
Этот пример простой прототип ui оболочки которую я хочу прикрутить к своему футбольному парсеру на selenium
"""


class Users:
    def __init__(self):
        self.file_path = 'users.json'
        self.users = read_json(file_path=self.file_path)

    def add_new_user(self, user_id, user_first_name, user_last_name) -> bool:
        user_id = str(user_id)
        if user_id in self.users:
            return False
        self.users[user_id] = {"first_name": user_first_name, "last_name": user_last_name}
        rec_json(file_path=self.file_path, data=self.users)
        return True


class ExtendBot(MyBot):
    def __init__(self):
        super().__init__()
        self.users = Users()  # создание класса с пользователями

    def handlers(self):
        super().handlers()

        @self.dp.message(Command("start"))
        async def cmd_start(message: Message):
            res = self.users.add_new_user(
                user_id=message.from_user.id,
                user_first_name=message.from_user.first_name,
                user_last_name=message.from_user.last_name
            )
            if res:
                await message.answer(f"{message.from_user.first_name}, добро пожаловать!")
            else:
                await message.answer(f"{message.from_user.first_name}, вы уже есть в БД!")

        @self.dp.message(Command("users"))
        async def cmd_users(message: Message):
            await message.answer(f"{self.users.users}")


if __name__ == '__main__':
    bot = ExtendBot()
    asyncio.run(bot.run_bot())
