import asyncio
from initial import MyBot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery

"""
Пример toggle button, с помощью inline клавиатуры интерактивно на месте изменяем статус (меняем текст на кнопке, чтобы
было видно что переключение произошло, например ✔ и ❌)

Ключевым инструментом здесь является edit_reply_markup для обновления inline клавиатуре, что будет более наглядно 
выглядеть для пользователя
"""


class ExtendBot(MyBot):
    def __init__(self):
        super().__init__()
        self.switch_status = True  # флажок который нужно изменять (в будущем это будет )

    def handlers(self):
        super().handlers()

        # точка отправки клавиатуры пользователю
        @self.dp.message(Command("menu"))
        async def cmd_test(message: Message):
            # отправка клавиатуры пользователю
            keyboard = self.create_inline_keyboard()  # генерация клавиатуры
            await message.answer(f"Меню:", reply_markup=keyboard)  # отправка кнопок reply_markup

        @self.dp.callback_query(lambda c: c.data and c.data.startswith("switch_"))
        async def process_callback(callback: CallbackQuery):
            await callback.answer()
            btn_id = callback.data  # получение callback даты закрепленной за кнопкой и ветвление действий
            if btn_id == "switch_1":
                self.switch_status = not self.switch_status
                keyboard = self.create_inline_keyboard()  # генерация клавиатуры
                await callback.message.edit_reply_markup(reply_markup=keyboard)  # изменение уже существующей клавиатуры

    # создание inline клавиатуры, (кнопки которые появляются в чате, и несут уже в себе текст callback_data)
    def create_inline_keyboard(self):
        builder = InlineKeyboardBuilder()
        btn_txt = "✅" if self.switch_status else "❌"
        builder.button(text=f"toggle status {btn_txt}", callback_data='switch_1')
        builder.adjust(1)
        return builder.as_markup()


if __name__ == '__main__':
    bot = ExtendBot()
    asyncio.run(bot.run_bot())
