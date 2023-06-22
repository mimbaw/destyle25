import asyncio
import time

from pyrogram import Client, filters, idle
from pyrogram.types.messages_and_media.message import Message
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid, MessageIdInvalid
import schedule
from threading import Thread

from config import config
from db import everyhour_job, get_everyday_message, get_everyweek_message, add_completed_task
from handler import message_userbot_handler, tags


config_file = 'config/config.json'
savings_file = 'config/tasks'

api_id = config.api_id
api_hash = config.api_hash
chat_id = config.chat_id
OK_SIGN = config.OK_SIGN
tasks = set()
tags = ['#задача', '#вопрос']
tags_b = ['#задача ', '#вопрос ']
app = Client("my_account", api_id, api_hash)
saved_messages = []


class Task:
    def __init__(self, forwarded_message_id, message_id, chat_id):
        self.forwarded_id = forwarded_message_id
        self.message_id = message_id
        self.chat_id = chat_id

    def __str__(self):
        return f"{self.forwarded_id} {self.message_id} {self.chat_id}\n"


@app.on_message(filters=filters.all)
async def message_handler(client, message: Message):
    global saved_messages
    if message.text == '/get_id':
        await app.send_message('me', str(message.chat.id))
        await message.delete()
    saved_message = await message_userbot_handler(message, app, saved_messages)
    if saved_message:
        if message.text and message.text not in tags:
            saved_messages.append(message.text.lower())
        elif message.caption and message.caption not in tags:
            saved_messages.append(message.caption.lower())
        add_task(saved_message, message)


def add_task(saved_message, message):
    tasks.add(Task(saved_message.id, message.id, message.chat.id))

def load_tasks():
    with open('config/tasks', 'r') as file:
        for i in file.readlines():
            tasks.add(Task(*map(int, i.split())))
    with open('config/saved_messages', 'r') as file:
        string = file.read().split('|')
        for i in string:
            saved_messages.append(i)


async def check_if_completed():
    print("Bot started.")
    need_to_delete = []
    while True:
        delete_list = []
        if len(tasks) != 0:
            task: Task
            try:
                for task in tasks:
                    try:
                        i = await app.get_messages(chat_id, task.forwarded_id)
                        message = await app.get_messages(task.chat_id, task.message_id)
                        if i.reactions is not None and len([x for x in i.reactions.reactions if x.emoji == OK_SIGN]) != 0:
                            need_to_delete.append((task, i, message))
                    except PeerIdInvalid :
                        delete_list.append(task)
                    except ChannelInvalid:
                        delete_list.append(task)
                    except MessageIdInvalid:
                        delete_list.append(task)
            except: continue
            for i in delete_list:
                tasks.remove(i)
            if len(need_to_delete) > 0:
                for i in need_to_delete:
                    try:
                        await i[1].delete()
                        await app.send_reaction(i[0].chat_id, i[0].message_id, OK_SIGN)
                        tasks.discard(i[0])
                        add_completed_task()
                    except: 
                        need_to_delete.remove(i)
                need_to_delete.clear()
        await asyncio.sleep(0.5)

async def save_tasks():
    while True:
        with open(savings_file, 'w') as file:
            file.writelines(map(str, tasks))
        with open('config/saved_messages', 'w') as file:
            string = ''
            for i in saved_messages:
                string += f'{i}|'
            file.write(string)
        await asyncio.sleep(10)


async def send_message(message):
    await app.send_message(chat_id, message)

def run_everyday_job():
    message = get_everyday_message()
    Thread(target=asyncio.run, args=(send_message(message),)).start()

def run_everyweek_job():
    message = get_everyweek_message()
    Thread(target=asyncio.run, args=(send_message(message),)).start()

def run_shedule():
    schedule.every().hour.at(':59').do(everyhour_job)
    schedule.every().day.at('18:00').do(run_everyday_job)
    schedule.every().sunday.at('18:01').do(run_everyweek_job)
    while True:
        schedule.run_pending()
        time.sleep(1)


async def main():
    load_tasks()
    await app.start()
    Thread(target=run_shedule).start()
    coroutine_task = asyncio.create_task(check_if_completed())
    idle_task = asyncio.create_task(idle())
    save_task = asyncio.create_task(save_tasks())
    await asyncio.gather(idle_task, save_task, coroutine_task)
    await app.stop()

if __name__ == '__main__':
    app.run(main())