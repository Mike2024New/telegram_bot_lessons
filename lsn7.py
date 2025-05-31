import asyncio
from initial import MyBot
from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

"""
Машина состояний - диалог с пользователем. Точнее ведение пользователя по диалоговому сценарию. Cуть его заключается 
в следующем:
-Создаётся класс который будет хранить в себе все эти состояния (класс создаётся на базе класса StatesGroup)
-В процессе диалогов в класс записываются данные полученные из текущего сообщения, и происходит переключение на следующий
атрибут класса.
И так происходит до конечного сообщения в котором просто извлекаются все данные записанные в машину состояний.
По сути это система линейного диалога с пробросом переменных.
===================================================================
ВАЖНО! ПРИ ПРОДАКШЕНЕ (РАЗМЕЩЕНИИ НА СЕРВЕР) ЛУЧШЕ ИСПОЛЬЗОВАТЬ ДРУГОЕ ХРАНИЛИЩЕ ПАМЯТИ А НЕ MEMORY_STORAGE, ТАК КАК
ПРИ ПЕРЕЗАГРУЗКЕ БОТА, ЭТО ХРАНИЛИЩЕ БУДЕТ УНИЧТОЖЕНО. КАК ВАРИАНТ МОЖНО ИСПОЛЬЗОВАТЬ REDIS_STORAGE.
"""


class ExtendBot(MyBot):
    class UserForm(StatesGroup):
        """в этом классе хранятся состояния пользователей в момент диалога"""
        name = State()
        age = State()

    def __init__(self):
        super().__init__()

    def handlers(self):
        super().handlers()

        # запуск диалога в рамках машины состояний
        @self.dp.message(Command("dialog"))
        async def cmd_menu(message: Message, state: FSMContext):
            await message.answer("Давайте познакомимся! Как вас зовут?")
            await state.set_state(self.UserForm.name)  # запускаем машину состояний с курсором на name

        # получение возраста пользователя
        @self.dp.message(self.UserForm.name)
        async def process_name(message: types.Message, state: FSMContext):
            await state.update_data(name=message.text)
            await message.answer("Отлично, теперь введите ваш возраст:")
            await state.set_state(self.UserForm.age)  # переставляем курсор машины состояний на следующий вопрос

        # конечный вопрос (получение информации)
        @self.dp.message(self.UserForm.age)
        async def process_age(message: types.Message, state: FSMContext):
            if not message.text.isdigit():
                await message.answer("Возраст должен быть числом! Попробуйте ещё раз")
                return

            data = await state.get_data()  # получение данных из машины состояний
            await message.answer(f"Спасибо, {data['name']}! Вам {message.text} лет. \nАнкета заполнена.")
            await state.clear()


if __name__ == '__main__':
    bot = ExtendBot()
    asyncio.run(bot.run_bot())
