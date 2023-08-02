# Импортируем модуль для работы с базой данных SQLite
import os
import sqlite3
import datetime

import openpyxl
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.greeting_keyboards import greeting_keyboards
from messages.greeting_post import greeting_post
from system.dispatcher import dp, bot

# Подключение к базе данных SQLite
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# Создание таблицы для заказов
cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  name TEXT,
                  phone TEXT,
                  link TEXT,
                  size TEXT,
                  color TEXT,
                  price TEXT,
                  date TEXT)''')
# Создаем таблицу, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        date TEXT
    )
''')

conn.commit()


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия"""
    await state.reset_state()

    # Получаем текущую дату и время
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Записываем данные пользователя в базу данных
    cursor.execute('''INSERT INTO users (user_id, first_name, last_name, username, date) VALUES (?, ?, ?, ?, ?)''', (
        message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username,
        current_date))
    conn.commit()

    print(f'Привет! нажали на кнопку /start {message.from_user.id, message.from_user.username, current_date}')

    keyboards_greeting = greeting_keyboards()
    # Клавиатура для Калькулятора цен или Контактов
    await message.reply(greeting_post, reply_markup=keyboards_greeting, disable_web_page_preview=True,
                        parse_mode=types.ParseMode.HTML)


# Обработчик команды /export
@dp.message_handler(commands=['export_user'])
async def export_command(message: types.Message):
    # Проверяем, является ли пользователь, который вызывает команду, администратором
    if message.from_user.id not in [5837917794, 5958542955]:
        await message.reply('У вас нет доступа к этой команде.')
        return
    # Получаем данные всех пользователей из базы данных
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    # Создаем файл Excel и записываем данные
    import openpyxl
    from openpyxl.utils import get_column_letter
    wb = openpyxl.Workbook()
    sheet = wb.active
    # Записываем заголовки
    headers = ['ID', 'User ID', 'First Name', 'Last Name', 'Username', 'Date']
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        sheet[f'{col_letter}1'] = header
    # Записываем данные пользователей
    for row_num, row_data in enumerate(data, 2):
        for col_num, cell_data in enumerate(row_data, 1):
            col_letter = get_column_letter(col_num)
            sheet[f'{col_letter}{row_num}'] = cell_data
    # Сохраняем файл Excel
    wb.save('users.xlsx')
    # Отправляем файл пользователю
    with open('users.xlsx', 'rb') as file:
        await bot.send_document(message.from_user.id, file, caption='Данные пользователей в формате Excel')
    # Удаляем файл Excel
    import os
    os.remove('users.xlsx')


# Создание класса состояний
class MakingAnOrder(StatesGroup):
    making_an_order = State()
    write_name = State()
    write_phone = State()
    write_link = State()
    write_size = State()
    write_color = State()
    write_price = State()


@dp.callback_query_handler(lambda c: c.data == "making_an_order")
async def order(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    greeting_post_on = ("Привет! Я бот для сбора данных заказа.\n\n"
                        "Пожалуйста, введите ваше имя:")
    await bot.send_message(callback_query.from_user.id, greeting_post_on)
    await MakingAnOrder.write_name.set()


# Обработчик ввода имени
@dp.message_handler(state=MakingAnOrder.write_name)
async def write_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await MakingAnOrder.next()
    await bot.send_message(message.from_user.id, "Пожалуйста, введите ваш номер телефона:")


# Обработчик номера телефона
@dp.message_handler(state=MakingAnOrder.write_phone)
async def write_phone(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)
    await MakingAnOrder.next()
    linc = (f"<a href='https://telegra.ph/Kak-sdelat-zakaz-05-03-2'>Как скопировать ссылку на товар?</a>\n\n"
            f"Пожалуйста, введите ссылку на товар:")
    await bot.send_message(message.from_user.id, linc, disable_web_page_preview=True, parse_mode=types.ParseMode.HTML)


# Обработчик ввода ссылки на товар
@dp.message_handler(state=MakingAnOrder.write_link)
async def write_link(message: types.Message, state: FSMContext):
    link = message.text
    await state.update_data(link=link)
    await MakingAnOrder.next()
    await bot.send_message(message.from_user.id, "Пожалуйста, введите размер товара:")


# Обработчик ввода размера товара
@dp.message_handler(state=MakingAnOrder.write_size)
async def write_size(message: types.Message, state: FSMContext):
    size = message.text
    await state.update_data(size=size)
    await MakingAnOrder.next()
    await bot.send_message(message.from_user.id, "Пожалуйста, введите цвет товара:")


# Обработчик ввода цвета товара
@dp.message_handler(state=MakingAnOrder.write_color)
async def write_color(message: types.Message, state: FSMContext):
    color = message.text
    await state.update_data(color=color)
    await MakingAnOrder.next()
    await bot.send_message(message.from_user.id, "Пожалуйста, введите цену товара:")


# Обработчик ввода цены товара
@dp.message_handler(state=MakingAnOrder.write_price)
async def write_price(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    # Получение текущей даты
    dat = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = await state.get_data()
    # Извлечение данных из состояния
    user_id = message.from_user.id
    name = data.get('name')
    phone = data.get('phone')
    link = data.get('link')
    size = data.get('size')
    color = data.get('color')
    price = data.get('price')
    # Сохранение данных в базу данных
    cursor.execute("INSERT INTO orders "
                   "(user_id, name, phone, link, size, color, price, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (user_id, name, phone, link, size, color, price, dat))
    conn.commit()
    await state.finish()
    order_details = (f"Спасибо за ваш заказ!\n\n"
                     f"Данные заказа были отправлены нашему менеджеру @poizon_commerce_manager\n\n"
                     f""f"Имя: {name}\n"
                     f"Номер телефона: {phone}\n"
                     f"Ссылка на товар: {link}\n"
                     f"Размер: {size}\n"
                     f"Цвет: {color}\n"
                     f"Цена: {price}"
                     "\n\nДля возврата в начало нажмите /start")
    await bot.send_message(message.from_user.id, order_details, disable_web_page_preview=True)

    # Определение данных о пользователе для отправки администратору
    user = message.from_user
    user_info = f"{user.first_name} "
    if user.last_name:
        user_info += f"{user.last_name} "
    if user.username:
        user_info += f"@{user.username}\n"

    admin_id = 5958542955  # Poizon менеджер
    # admin_id = 5837917794  # @PyAdminRUS

    order_details_admin = (f"Заказ от: {user_info}\n"
                           f"Номер телефона: {phone}\n"
                           f"Ссылка на товар: {link}\n"
                           f"Размер: {size}\n"
                           f"Цвет: {color}\n"
                           f"Цена: {price}")
    await bot.send_message(admin_id, order_details_admin, disable_web_page_preview=True)


# Функция для создания файла Excel с данными заказов
def create_excel_file(orders):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    # Заголовки столбцов
    sheet['A1'] = 'ID'
    sheet['B1'] = 'User ID'
    sheet['C1'] = 'Имя'
    sheet['D1'] = 'Номер телефона'
    sheet['E1'] = 'Ссылка на товар'
    sheet['F1'] = 'Размер'
    sheet['G1'] = 'Цвет товара'
    sheet['H1'] = 'Цена на товар в юанях'
    sheet['I1'] = 'Дата заказа'
    # Заполнение данными заказов
    for index, order in enumerate(orders, start=2):
        sheet.cell(row=index, column=1).value = order[0]  # ID
        sheet.cell(row=index, column=2).value = order[1]  # User ID
        sheet.cell(row=index, column=3).value = order[2]  # Name
        sheet.cell(row=index, column=4).value = order[3]  # Phone
        sheet.cell(row=index, column=5).value = order[4]  # Link
        sheet.cell(row=index, column=6).value = order[5]  # Size
        sheet.cell(row=index, column=7).value = order[6]  # Color
        sheet.cell(row=index, column=8).value = order[7]  # Price
        sheet.cell(row=index, column=9).value = order[8]  # Date

    return workbook


# Обработчик команды для выгрузки данных в Excel
@dp.message_handler(commands=['export_orders'])
async def export_data(message: types.Message):
    if message.from_user.id not in [5837917794, 5958542955]:
        await message.reply('У вас нет доступа к этой команде.')
        return
    # Получение данных из базы данных
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    # Создание файла Excel
    workbook = create_excel_file(orders)
    # Сохранение файла
    filename = 'orders.xlsx'
    workbook.save(filename)
    # Отправка файла пользователю
    with open(filename, 'rb') as file:
        await message.answer_document(file)
    # Удаление файла
    os.remove(filename)


def greeting_handler():
    """Регистрируем handlers для калькулятора"""
    dp.register_message_handler(greeting)  # Обработчик команды /start, он же пост приветствия
