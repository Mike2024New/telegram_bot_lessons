import asyncio
from initial import MyBot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery

"""
реализация toggle button для группы переключателей
"""


class ExtendBot(MyBot):
    def __init__(self):
        super().__init__()
        # переключатели, условно говоря ключ здесь является и callback датой (здесь просто упрощено)
        self.switches = {
            "switch_1": False,
            "switch_2": False,
            "switch_3": False
        }  # такая структура гарантирует мне расширяемость

    def handlers(self):
        super().handlers()

        @self.dp.message(Command("menu"))
        async def cmd_menu(message: Message):
            keboard = self.create_inline_keyboard()
            await message.answer(f"Меню переключателей:", reply_markup=keboard)

        @self.dp.callback_query(lambda c: c.data and c.data.startswith("switch_"))
        async def process_callback(callback: CallbackQuery):
            await callback.answer()
            btn_id = callback.data  # получаем текущую callback.data
            self.switches[btn_id] = not self.switches[btn_id]  # изменяем значение на противоположную
            keyboard = self.create_inline_keyboard()
            await callback.message.edit_reply_markup(reply_markup=keyboard)

    def create_inline_keyboard(self):
        builder = InlineKeyboardBuilder()
        for key in self.switches:
            btn_txt = "✅" if self.switches[key] else "❌"
            builder.button(text=btn_txt, callback_data=key)
        builder.adjust(3)
        return builder.as_markup()


if __name__ == '__main__':
    bot = ExtendBot()
    asyncio.run(bot.run_bot())
