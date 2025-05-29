import os
import logging
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = os.getenv('MY_TEST_REP_BOT')
if TOKEN is None:
    raise RuntimeError("Переменная окружения MY_TEST_REP_BOT не установлена")


class MyBot:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)  # запускаем логирование
        self.bot = Bot(TOKEN)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.handlers()  # регистрация обработчиков при инициализации (она должна происходить до запуска бота)
        self.unknow_command_handlers()  # регистрация обработчика не определенной команды

    def handlers(self):
        @self.dp.message(Command("start"))
        async def cmd_start(message: Message):
            await message.answer(f"Тестовый запуск. Ваш id: {message.from_user.id}")

        @self.dp.message(Command("stop"))
        async def cmd_stop(message: Message):
            # убираем все инициализированные ранее клавиатуры
            await message.answer("Бот остановлен")
            await self.dp.stop_polling()
            await self.bot.session.close()

    def unknow_command_handlers(self):
        @self.dp.message()  # обработчик если команда не распознана
        async def cmd_unknow(message: Message):
            await message.answer(f"неизвестная комманда {message.text}, попробуйте ещё, ладно?")

    async def run_bot(self):
        # drop_pending_updates все сообщения полученные в простой бота игнорируются
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)  # запускаем бота (polling это значит опрос сервера telegram)
