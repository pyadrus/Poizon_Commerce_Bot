from aiogram import types

from messages.message_text_faq import message_text_faq
from system.dispatcher import dp, bot


@dp.callback_query_handler(lambda c: c.data == 'faq')
async def faq_handler(callback_query: types.CallbackQuery):
    """Пояснение для пользователя FAQ"""
    with open('media/photos/faq.jpg', 'rb') as photo_file: # Загружаем фото для поста
        # Если отправляется фото, то не отображается превью ссылок
        await bot.send_photo(callback_query.from_user.id, photo=photo_file, caption=message_text_faq,
                             parse_mode=types.ParseMode.HTML)


def faq_handlers():
    """Регистрируем handlers для FAQ"""
    dp.register_message_handler(faq_handler)
