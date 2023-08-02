from aiogram import executor

from handlers.contacts import contacts_handlers
from handlers.faq import faq_handlers
from handlers.greeting import greeting_handler
from handlers.price_calculator import price_calculator_handler
from system.dispatcher import dp


def main():
    executor.start_polling(dp, skip_updates=True)
    price_calculator_handler()
    greeting_handler()
    faq_handlers()  # Пояснение для пользователя FAG
    contacts_handlers()


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        print(e)
