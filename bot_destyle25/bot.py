import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import requests

from config import config
from handler import check_old_messages


bot = Bot(config.token)
dp = Dispatcher(bot, storage=MemoryStorage())


def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton("Проверка старых сообщений", callback_data="check_messages")
    button_2 = types.InlineKeyboardButton("Задачи по именам", callback_data="by_names")
    button_3 = types.InlineKeyboardButton("Задачи по времени", callback_data="tasks_by_time")
    button_4 = types.InlineKeyboardButton("Решения по временам", callback_data="decision_by_time")
    keyboard.add(button_1)
    keyboard.add(button_2, button_3)
    keyboard.add(button_4)
    return keyboard

def get_tasks_keyboard(filter):
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton("За день", callback_data=f"{filter}_tasks_for_day")
    button_2 = types.InlineKeyboardButton("За неделю", callback_data=f"{filter}_tasks_for_week")
    button_3 = types.InlineKeyboardButton("За меясяц", callback_data=f"{filter}_tasks_by_month")
    button_4 = types.InlineKeyboardButton("За год", callback_data=f"{filter}_tasks_for_year")
    button_5 = types.InlineKeyboardButton("Назад", callback_data="back")
    keyboard.add(button_1, button_2)
    keyboard.add(button_3, button_4)
    keyboard.add(button_5)
    return keyboard

def get_decision_by_time_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton("За день", callback_data="decision_for_day")
    button_2 = types.InlineKeyboardButton("За неделю", callback_data="decision_for_week")
    button_3 = types.InlineKeyboardButton("За меясяц", callback_data="decision_by_month")
    button_4 = types.InlineKeyboardButton("За год", callback_data="decision_for_year")
    button_5 = types.InlineKeyboardButton("Назад", callback_data="back")
    keyboard.add(button_1, button_2)
    keyboard.add(button_3, button_4)
    keyboard.add(button_5)
    return keyboard

def get_back_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton("Назад!", callback_data="back")
    keyboard.add(button_1)
    return keyboard


class FSM_machine(StatesGroup):
    value = State()


@dp.message_handler(commands='start')
async def start_handler(message: types.Message):
    await message.answer('Привет!', reply_markup=get_main_keyboard())

@dp.channel_post_handler()
async def test(message: types.Message):
    if message.text == '/start':
        await message.answer('Привет!', reply_markup=get_main_keyboard())


@dp.channel_post_handler(state=FSM_machine.value)
async def fsm_chanell_message_handler(message: types.Message, state: FSMContext):
    if '.' in message.text and len(message.text) in range(8, 11):
        await message.answer("Процесс успешно запущен")
        date = message.text.split('.')
        cnt = await check_old_messages(date)
        string = f"Процесс успешно завершен. Всего найдено {cnt} необработанных сообщений"
        print(string)
        await bot.send_message(message.chat.id, string, reply_markup=get_back_keyboard())
        await state.finish()
    else:
        await state.reset_state()
        await FSM_machine.value.set()
        await message.answer('Неправильный формат данных! Слуедующим сообщением отправьте ограничение по дате. Пример: 10.1.2023. Без нулей в начале!', reply_markup=get_back_keyboard())

@dp.message_handler(content_types=['text'], state=FSM_machine.value)
async def checker_old_messager(message: types.Message, state: FSMContext):
    if '.' in message.text and len(message.text) in range(8, 11):
        await message.answer("Процесс успешно запущен")
        date = message.text.split('.')
        cnt = await check_old_messages(date)
        string = f"Процесс успешно завершен. Всего найдено {cnt} необработанных сообщений"
        print(string)
        await bot.send_message(message.chat.id, string, reply_markup=get_back_keyboard())
        await state.finish()
    else:
        await state.reset_state()
        await FSM_machine.value.set()
        await message.answer('Неправильный формат данных! Слуедующим сообщением отправьте ограничение по дате. Пример: 10.1.2023. Без нулей в начале!', reply_markup=get_back_keyboard())


@dp.callback_query_handler(state=FSM_machine.value)
async def fsm_call_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await state.reset_state()
        await call.message.edit_text("Привет!", reply_markup=get_main_keyboard())

@dp.callback_query_handler()
async def messages_handler(call: types.CallbackQuery):
    if call.data == "check_messages":
        await FSM_machine.value.set()
        await call.message.edit_text("Следующим сообщением отправьте ограничение по дате. Пример: 10.1.2023. Без нулей в начале!", reply_markup=get_back_keyboard())
    elif call.data == "back":
        await call.message.edit_text("Привет!", reply_markup=get_main_keyboard())
    elif call.data == "by_names":
        await call.message.edit_text("Задачи по именам:", reply_markup=get_tasks_keyboard('name'))
    elif call.data == "tasks_by_time":
        await call.message.edit_text("Задачи по времени:", reply_markup=get_tasks_keyboard('time'))
    elif call.data == "decision_by_time":
        await call.message.edit_text("Решения по времени:", reply_markup=get_decision_by_time_keyboard())

    elif "name" in call.data:
        string = '*Количество поставленных задач:*'
        if "day" in call.data:
            data = requests.post('http://localhost:8080', data="name_tasks_for_day").json()['response']
        elif "week" in call.data:
            data = requests.post('http://localhost:8080', data='name_tasks_for_week').json()['response']      
        elif "month" in call.data:
            data = requests.post('http://localhost:8080', data='name_tasks_for_month').json()['response']   
        elif "year" in call.data:
            data = requests.post('http://localhost:8080', data='name_tasks_for_year').json()['response']   
        for i in data:
            if i[2] != 0:
                if i[1] != 'None':
                    string += f"\n\U000000B7 {i[0]} {i[1]} - *{i[2]}*"
                else:
                    string += f"\n\U000000B7 {i[0]} - *{i[2]}*"
        await call.message.edit_text(string, "MARKDOWN", reply_markup=get_back_keyboard())

    elif "time" in call.data:
        string = '*Количество задач по времени:*'
        if "day" in call.data:
            data = requests.post('http://localhost:8080', data='time_tasks_for_day').json()['response']
        elif "week" in call.data:
            data = requests.post('http://localhost:8080', data='time_tasks_for_week').json()['response']      
        elif "month" in call.data:
            data = requests.post('http://localhost:8080', data='time_tasks_for_month').json()['response']
        elif "year" in call.data:
            data = requests.post('http://localhost:8080', data='time_tasks_for_year').json()['response']
        for i in data.keys():
            if "day" in call.data:
                if data[i] != '0':
                    string += f"\n\U000000B7 {i} - {data[i]}"
            else:
                if data[i]:
                    string += f"\n\U000000B7 {i} - {data[i]}"
                else:
                    string += f"\n\U000000B7 {i} - {0}"
        await call.message.edit_text(string, "MARKDOWN", reply_markup=get_back_keyboard())

    elif "decision" in call.data:
        string = '*Решения по времени:*'
        if "day" in call.data:
            data = requests.post('http://localhost:8080', data='decision_for_day').json()['response']
        elif "week" in call.data:
            data = requests.post('http://localhost:8080', data='decision_for_week').json()['response']    
        elif "month" in call.data:
            data = requests.post('http://localhost:8080', data='decision_for_month').json()['response']
        elif "year" in call.data:
            data = requests.post('http://localhost:8080', data='decision_for_year').json()['response']
        for i in data.keys():
            if "day" in call.data:
                if data[i] != '0':
                    string += f"\n\U000000B7 {i} - {data[i]}"
            else:
                if data[i]:
                    string += f"\n\U000000B7 {i} - {data[i]}"
                else:
                    string += f"\n\U000000B7 {i} - {0}"
        await call.message.edit_text(string, "MARKDOWN", reply_markup=get_back_keyboard())
            

async def run_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run_bot())