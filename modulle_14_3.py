from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

api = ""

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()

button_calc = KeyboardButton(text="Рассчитать")
button_info = KeyboardButton(text="Информация")
button_buy = KeyboardButton(text="Купить")

kb.add(button_calc)
kb.add(button_info)
kb.add(button_buy)


ikb = InlineKeyboardMarkup()
in_button_calc = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button_get_formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

ikb.add(in_button_calc)
ikb.add(in_button_get_formulas)



ikb_product_list = InlineKeyboardMarkup()

btn_p_first = InlineKeyboardButton(text="Product1", callback_data="product_buying")
btn_p_second = InlineKeyboardButton(text="Product2", callback_data="product_buying")
btn_p_third = InlineKeyboardButton(text="Product3", callback_data="product_buying")
btn_p_fourth = InlineKeyboardButton(text="Product4", callback_data="product_buying")

ikb_product_list.add(btn_p_first)
ikb_product_list.add(btn_p_second)
ikb_product_list.add(btn_p_third)
ikb_product_list.add(btn_p_fourth)



kb.resize_keyboard = True


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)



@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('.venv/files/Product1.png', 'rb') as img:
        await message.answer(f'Название: Product1 | Описание: описание 1 | Цена: {1 * 100}')
        await message.answer_photo(img)

    with open('.venv/files/Product2.png', 'rb') as img:
        await message.answer(f'Название: Product2 | Описание: описание 2 | Цена: {2 * 100}')
        await message.answer_photo(img)

    with open('.venv/files/Product3.png', 'rb') as img:
        await message.answer(f'Название: Product3 | Описание: описание 3 | Цена: {3 * 100}')
        await message.answer_photo(img)

    with open('.venv/files/Product4.png', 'rb') as img:
        await message.answer(f'Название: Product4 | Описание: описание 4 | Цена: {4 * 100}')
        await message.answer_photo(img)

    await message.answer("Выберите товар для покупки:", reply_markup=ikb_product_list)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))
    calories = 10 * weight + 6.25 * growth - 5 * age + 5  # Сайт из задания не работал, поэтому искал в инете:  (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5)
    await message.answer(f'Ваша норма калорий: {calories:.2f} ккал в день.')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
