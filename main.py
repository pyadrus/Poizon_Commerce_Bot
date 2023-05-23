import configparser
import logging

from aiogram import Bot, Dispatcher
from aiogram import executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.inline_keyboards import clothing_keyboard, delivery_keyboard
from services.exchange import get_currency_rate
from utils.validation import calculate_insurance_price, calculate_commission_price

config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
config.read("setting/config.ini")
bot_token = config.get('BOT_TOKEN', 'BOT_TOKEN')

bot = Bot(token=bot_token, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    await state.reset_state()  # Сброс состояния бота
    keyboard_clothes = clothing_keyboard()
    await message.reply("Выберите тип товара:", reply_markup=keyboard_clothes)


"""Тип одежды для определения веса"""


@dp.callback_query_handler(lambda c: c.data == 'footwear')
async def calculate_cost_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик расчета стоимости для 👟 Обувь"""
    delivery = delivery_keyboard()
    await bot.send_message(callback_query.from_user.id, "Выберите тип доставки:", reply_markup=delivery)
    exchange_rate = 1
    await state.update_data(exchange_rate=exchange_rate)  # Функция для обновления данных в состоянии, аналог return


@dp.callback_query_handler(lambda c: c.data == 'trousers')
async def calculate_cost_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик расчета стоимости для 👖 Штаны"""
    delivery = delivery_keyboard()
    await bot.send_message(callback_query.from_user.id, "Выберите тип доставки:", reply_markup=delivery)
    exchange_rate = 0.8
    await state.update_data(exchange_rate=exchange_rate)  # Функция для обновления данных в состоянии, аналог return


@dp.callback_query_handler(lambda c: c.data == 'hoodies')
async def calculate_cost_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик расчета стоимости для 🥼 Худи"""
    delivery = delivery_keyboard()
    await bot.send_message(callback_query.from_user.id, "Выберите тип доставки:", reply_markup=delivery)
    exchange_rate = 1
    await state.update_data(exchange_rate=exchange_rate)  # Функция для обновления данных в состоянии, аналог return


@dp.callback_query_handler(lambda c: c.data == 'down_jacket_down')
async def calculate_cost_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик расчета стоимости для 🧥 Пуховик (пух)"""
    delivery = delivery_keyboard()
    await bot.send_message(callback_query.from_user.id, "Выберите тип доставки:", reply_markup=delivery)
    exchange_rate = 2
    await state.update_data(exchange_rate=exchange_rate)  # Функция для обновления данных в состоянии, аналог return


@dp.callback_query_handler(lambda c: c.data == 'down_jacket_synthetic')
async def calculate_cost_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик расчета стоимости для 🧥 Пуховик (синтетика)"""
    delivery = delivery_keyboard()
    await bot.send_message(callback_query.from_user.id, "Выберите тип доставки:", reply_markup=delivery)
    exchange_rate = 1.2
    await state.update_data(exchange_rate=exchange_rate)  # Функция для обновления данных в состоянии, аналог return


@dp.callback_query_handler(lambda c: c.data == 'backpack')
async def calculate_cost_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик расчета стоимости для 🎒 Рюкзак"""
    delivery = delivery_keyboard()
    await bot.send_message(callback_query.from_user.id, "Выберите тип доставки:", reply_markup=delivery)
    exchange_rate = 0.6
    await state.update_data(exchange_rate=exchange_rate)  # Функция для обновления данных в состоянии, аналог return


@dp.callback_query_handler(lambda c: c.data == 'shoulder_bag')
async def calculate_cost_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик расчета стоимости для 👜 Сумка наплечная"""
    delivery = delivery_keyboard()
    await bot.send_message(callback_query.from_user.id, "Выберите тип доставки:", reply_markup=delivery)
    exchange_rate = 0.2
    await state.update_data(exchange_rate=exchange_rate)  # Функция для обновления данных в состоянии, аналог return


@dp.callback_query_handler(lambda c: c.data == 'longsleeve')
async def calculate_cost_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик расчета стоимости для 👕 Лонгслив / майка"""
    delivery = delivery_keyboard()
    await bot.send_message(callback_query.from_user.id, "Выберите тип доставки:", reply_markup=delivery)
    exchange_rate = 0.4
    await state.update_data(exchange_rate=exchange_rate)  # Функция для обновления данных в состоянии, аналог return


"""Виды доставки"""


@dp.callback_query_handler(lambda c: c.data == 'scheduled_aircraft')
async def process_delivery_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Ввод пользователем цены товара в рублях"""
    await bot.send_message(callback_query.from_user.id,
                           "Введите цену товара в юанях 🇨🇳 (копейки указываются через точку):")
    usd_rate = get_currency_rate('USD')  # Курс Доллара к рублю
    data = await state.get_data()
    exchange_rate = data.get('exchange_rate', 0)
    shipping_cost = (35 * usd_rate) * exchange_rate
    await state.update_data(shipping_cost=shipping_cost)  # Функция для обновления данных в состоянии, аналог return


@dp.callback_query_handler(lambda c: c.data == 'scheduled_aircraft')
async def process_delivery_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Ввод пользователем цены товара в рублях"""
    await bot.send_message(callback_query.from_user.id,
                           "Введите цену товара в юанях 🇨🇳 (копейки указываются через точку):")
    usd_rate = get_currency_rate('USD')  # Курс Доллара к рублю
    data = await state.get_data()
    exchange_rate = data.get('exchange_rate', 0)
    shipping_cost = (12 * usd_rate) * exchange_rate
    await state.update_data(shipping_cost=shipping_cost)  # Функция для обновления данных в состоянии, аналог return


@dp.callback_query_handler(lambda c: c.data == 'a_regular_truck')
async def process_delivery_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Ввод пользователем цены товара в рублях"""
    await bot.send_message(callback_query.from_user.id,
                           "Введите цену товара в юанях 🇨🇳 (копейки указываются через точку):")
    usd_rate = get_currency_rate('USD')  # Курс Доллара к рублю
    data = await state.get_data()
    exchange_rate = data.get('exchange_rate', 0)
    shipping_cost = (6 * usd_rate) * exchange_rate
    await state.update_data(shipping_cost=shipping_cost)  # Функция для обновления данных в состоянии, аналог return


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_price(message: types.Message, state: FSMContext):
    try:
        cny_rate = get_currency_rate('CNY')  # Курс Юаня к рублю
        price = float(message.text)  # Цена товара в Юанях введенная пользователем
        delivery_rub_cn = 30 * cny_rate  # Цена доставки Poizon до склада в Китай
        insurance_price = calculate_insurance_price(price)  # Расчет стоимости страховки
        commission_price = calculate_commission_price(price)  # Расчет стоимости комиссии
        data = await state.get_data()
        shipping_cost = data.get('shipping_cost', 0)

        # Рассчитываем итоговую стоимость приобретения
        final_purchase_price = (price * cny_rate) + delivery_rub_cn + insurance_price + shipping_cost + commission_price
        rounded_number = round(final_purchase_price, 2)  # Округляем до 2х знаков
        message_text = f"<b>Общая стоимость: {rounded_number} руб.</b>\n\nДля возврата в начало нажмите /start"
        await bot.send_message(message.chat.id, message_text)
        await state.finish()
    except ValueError:
        await bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
