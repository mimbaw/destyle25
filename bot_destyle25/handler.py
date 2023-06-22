import asyncio
from pyrogram import Client, idle
from pyrogram.enums.parse_mode import ParseMode
from datetime import datetime, timedelta

from config import config


api_id = config.api_id
api_hash = config.api_hash
chat_id = config.chat_id
tasks = set()
OK_SIGN = '👌'
app = Client("account_1", api_id, api_hash)

tags = ['#задача', '#вопрос']
tags_b = ['#задача ', '#вопрос ']

class Task:
    def __init__(self, forwarded_message_id, message_id, chat_id):
        self.forwarded_id = forwarded_message_id
        self.message_id = message_id
        self.chat_id = chat_id

    def __str__(self):
        return f"{self.forwarded_id} {self.message_id} {self.chat_id}\n"


def load_tasks():
    with open('config/tasks', 'r') as file:
        for i in file.readlines():
            tasks.add(Task(*map(int, i.split())))

async def check_if_completed():
    print("Bot started.")
    need_to_delete = []
    while True:
        if len(tasks) != 0:
            task: Task
            try:
                for task in tasks:
                    i = await app.get_messages(chat_id, task.forwarded_id)
                    if i.reactions is not None and len([x for x in i.reactions.reactions if x.emoji == config.OK_SIGN]) != 0:
                        need_to_delete.append((task, i))
            except: continue
            if len(need_to_delete) > 0:
                for i in need_to_delete:
                    try:
                        await app.send_reaction(i[0].chat_id, i[0].message_id, config.OK_SIGN)
                        tasks.discard(i[0])
                        await i[1].delete()
                    except:
                        continue
                need_to_delete.clear()
        await asyncio.sleep(0.5)

async def save_tasks():
    while True:
        with open('config/tasks', 'w') as file:
            file.writelines(map(str, tasks))
        await asyncio.sleep(60)

def add_task(saved_message, message):
    tasks.add(Task(saved_message.id, message.id, message.chat.id))

async def run_handler():
    load_tasks()
    await app.start()
    coroutine_task = asyncio.create_task(check_if_completed())
    idle_task = asyncio.create_task(idle())
    save_task = asyncio.create_task(save_tasks())
    await asyncio.gather(idle_task, save_task, coroutine_task)
    await app.stop()


async def check_old_messages(date_list=None):
    cnt = 0
    async for dialog in app.get_dialogs():
        if dialog.chat.id == chat_id:
            continue
        date_message_id = 0
        async for message in app.get_chat_history(dialog.chat.id, 1, offset_date=datetime(int(date_list[2]), int(date_list[1]), int(date_list[0]))):
            date_message_id = message.id
        async for message in app.get_chat_history(dialog.chat.id):
            if message.id == date_message_id:
                break
            if message.reactions is None or len([x for x in message.reactions.reactions if x.emoji == OK_SIGN]) == 0 and message.chat.id != chat_id:
                #try:
                date = message.date
                date += timedelta(hours=5, minutes=30)
                date = date.strftime("%d.%m в %H:%M")
                if message.text:
                    if message.text.lower() in tags: # если сообщение есть только тэг, то берется предыдущее сообщение
                        async for i in app.get_chat_history(message.chat.id, limit=1, offset_id=message.id):
                            previous_message = i
                        if previous_message.text: # если предыдущее сообщение есть текст
                            string = f'{message.text}\n{previous_message.text} <i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_message(chat_id, string, ParseMode.HTML, disable_web_page_preview=True)
                        
                        elif previous_message.photo: # если предыдущее сообщение есть фото
                            if previous_message.caption:
                                string = f'{message.text}\n{previous_message.caption} <i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'

                            else:
                                string = f'{message.text}\n<i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'

                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_photo(chat_id, previous_message.photo.file_id, string, ParseMode.HTML)
                    
                        elif previous_message.voice: # если предыдущее сообщение есть голосовое
                            string = f'{message.text}\n<i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_voice(chat_id, previous_message.voice.file_id, string, ParseMode.HTML)

                        elif previous_message.document:# если предыдущее сообщение есть документ
                            if previous_message.caption:
                                string = f'{message.text}\n{previous_message.caption} <i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                            
                            else:
                                string = f'{message.text}\n<i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'

                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_document(chat_id, previous_message.document.file_id, caption=string, parse_mode=ParseMode.HTML) 

                        print('Задача сохранена в группе.')
                        add_task(saved_message, message)
                        cnt+=1

                    elif (any(tag in message.text.lower() for tag in tags) and ((any(message.text.lower().split(tag)[-1] == '' for tag in tags)) or any(message.text.lower().split(tag)[-1][0] == '\n' for tag in tags))) or any(tag in message.text.lower() for tag in tags_b): # Если в сообщении не только тег
                        string = f'{message.text}\n\n____\n{message.from_user.mention} - {date}'
                        if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                            string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                        if message.chat.type.name == 'GROUP':
                            string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                        if message.chat.type.name == 'PRIVATE':
                            string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                        saved_message = await app.send_message(chat_id, string, ParseMode.HTML, disable_web_page_preview=True)
                        print('Задача сохранена в группе.')
                        add_task(saved_message, message)
                        cnt+=1

                elif message.photo: # если сообщение есть фото
                    if message.caption: # если у фото есть описание
                        if message.caption.lower() in tags: # если в описании только тэг
                            async for i in app.get_chat_history(message.chat.id, limit=1, offset_id=message.id):
                                previous_message = i
                            if previous_message.text: # если предыдущее сообщение есть текст
                                string = f'{message.caption}\n{previous_message.text} <i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_photo(chat_id, message.photo.file_id, string, ParseMode.HTML)
                            
                            elif previous_message.photo: # если предыдущее сообщение есть фото
                                if previous_message.caption:
                                    string = f'{message.caption}\n{previous_message.caption} <i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'

                                else:
                                    string = f'{message.caption}\n\n____\n{message.from_user.mention} - {date}'

                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_photo(chat_id, message.photo.file_id, string, ParseMode.HTML)
                        
                            elif previous_message.voice: # если предыдущее сообщение есть голосовое
                                string = f'{message.caption}\n\n____\n{message.from_user.mention} - {date}'
                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_photo(chat_id, message.photo.file_id, string, ParseMode.HTML)

                            elif previous_message.document:# если предыдущее сообщение есть документ
                                if previous_message.caption:
                                    string = f'{message.caption}\n{previous_message.caption} <i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                
                                else:
                                    string = f'{message.caption}\n\n____\n{message.from_user.mention} - {date}'

                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_photo(chat_id, message.photo.file_id, string, ParseMode.HTML) 

                            print('Задача сохранена в группе.')
                            add_task(saved_message, message)
                            cnt+=1

                        elif (any(tag in message.caption.lower() for tag in tags) and ((any(message.caption.lower().split(tag)[-1] == '' for tag in tags)) or any(message.caption.lower().split(tag)[-1][0] == '\n' for tag in tags))) or any(tag in message.caption.lower() for tag in tags_b):  # если в описании есть тэг и какой-то текст
                            string = f'{message.caption}\n\n____\n{message.from_user.mention} - {date}'
                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_photo(chat_id, message.photo.file_id, string, ParseMode.HTML)
                            print('Задача сохранена в группе.')
                            add_task(saved_message, message)
                            cnt+=1

                elif message.document:
                    if message.caption: # если у документа есть описание
                        if message.caption.lower() in tags: # если в описании только тэг
                            async for i in app.get_chat_history(message.chat.id, limit=1, offset_id=message.id):
                                previous_message = i
                            if previous_message.text: # если предыдущее сообщение есть текст
                                string = f'{message.caption}\n{previous_message.text} <i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_document(chat_id, message.document.file_id, caption=string, parse_mode=ParseMode.HTML)
                            
                            elif previous_message.photo: # предыдущее сообщение есть фото
                                if previous_message.caption: # если у предыдущего сообщения есть описание
                                    string = f'{message.caption}\n{previous_message.caption} <i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                else:
                                    string = f'{message.caption}\n<i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'

                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_document(chat_id, message.document.file_id, caption=string, parse_mode=ParseMode.HTML)

                            elif previous_message.document:
                                if previous_message.caption:
                                    string = f'{message.caption}\n{previous_message.caption} <i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                
                                else:
                                    string = f'{message.caption}\n<i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                
                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_document(chat_id, message.document.file_id, caption=string, parse_mode=ParseMode.HTML) 

                            print('Задача сохранена в группе.')
                            add_task(saved_message, message)
                            cnt+=1

                        elif (any(tag in message.caption.lower() for tag in tags) and ((any(message.caption.lower().split(tag)[-1] == '' for tag in tags)) or any(message.caption.lower().split(tag)[-1][0] == '\n' for tag in tags))) or any(tag in message.caption.lower() for tag in tags_b):  # если в описании есть тэг и какой-то текст
                            string = f'{message.caption}\n\n____\n{message.from_user.mention} - {date}'
                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_document(chat_id, message.document.file_id, caption=string, parse_mode=ParseMode.HTML)
                            print('Задача сохранена в группе.')
                            add_task(saved_message, message)
                            cnt+=1

                #except Exception as err:
                    #print(message.text)
                    #print(err)

    return cnt