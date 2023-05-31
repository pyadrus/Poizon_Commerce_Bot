from aiogram import types

from system.dispatcher import dp, bot
from texts.greeting_texts import contacts_post


@dp.callback_query_handler(lambda c: c.data == 'contacts')
async def contacts_handler(callback_query: types.CallbackQuery):
    """Контакты для связи"""
    await bot.send_message(callback_query.from_user.id, contacts_post, parse_mode=types.ParseMode.HTML)


def contacts_handlers():
    """Регистрируем handlers для калькулятора"""
    dp.register_message_handler(contacts_handler)  # Пояснение для пользователя FAG
