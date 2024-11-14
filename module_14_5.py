from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import MediaGroup
from crud_functions_14_5 import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


initiate_db()
check_and_products()
products = get_all_products()



menu_in = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying'),
        InlineKeyboardButton(text='Product2', callback_data='product_buying'),
        InlineKeyboardButton(text='Product3', callback_data='product_buying'),
        InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ]
)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for product in products:
        id_, title, description, price = product
        await message.answer (F'Название: {title} | Описание: {description} | Цена: {price}p')
        await message.answer_photo(photo=open(f'Vitamin{id_}.png', 'rb'))
    await message.answer('Выберите продукт для покупки:', reply_markup=menu_in )


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()




# @dp.message_handler(text=['Calories', 'Калории'])
@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(text='Информация')
async def  info(message):
    await message.answer( 'Я бот помогающий рассчитать необходимое количество потребляемых калорий ')




@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        age = float(data['age'])
        weight = float(data['weight'])
        growth = float(data['growth'])
    except:
        await message.answer(f'Не могу конвертировать введенные значения в числа.')
        await state.finish()
        return
    calories= 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'для мужчины норма: {calories} ккал')
    await state.finish()

@dp.message_handler(commands=['start'])
async def start(message):
    button_1 = KeyboardButton(text='Рассчитать')
    button_2 = KeyboardButton(text='Информация')
    button_3 = KeyboardButton(text='Купить')
    button_4 = KeyboardButton(text='Регистрация')
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder='Введите данные ')
    keyboard.insert(button_1)
    keyboard.insert(button_2)
    keyboard.add(button_3)
    keyboard.insert(button_4)
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=keyboard)
#    print('Привет! Я бот помогающий твоему здоровью.')

# ---- Регистрация пользователя -----
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    data = await state.get_data()

    name = is_included(data['username'])
    if name is True:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    print(data)
    add_user(data['username'], data['email'], data['age'])
    await message.answer("Регистрация прошла успешно!")
    await state.finish()




@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')
#    print('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
