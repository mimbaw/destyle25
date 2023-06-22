from pyrogram.types.messages_and_media.message import Message
from pyrogram.enums.parse_mode import ParseMode
from datetime import timedelta

from config.config import chat_id
from db import add_user_task


tags = ['#задача', '#вопрос']
tags_b = ['#задача ', '#вопрос ']

async def message_userbot_handler(message: Message, app, saved_messages):
        try:
            saved_message = ''
            date = message.date
            date += timedelta(hours=5, minutes=30)
            date = date.strftime("%d.%m в %H:%M")
            if message.text:
                if message.text.lower() in tags: # если сообщение есть только тег
                    if message.reply_to_message:
                        if message.reply_to_message.text: # ответ на текстовое сообщение
                            string = f'{message.text}\n{message.reply_to_message.text} <i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_message(chat_id, string, ParseMode.HTML, disable_web_page_preview=True)

                        elif message.reply_to_message.photo: # ответ на фото
                            if message.reply_to_message.caption: # ответ на фото с описанием
                                    string = f'{message.text}\n{message.reply_to_message.caption} <i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'

                            else: # ответ на фото без описания
                                string = f'{message.text}\n<i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'

                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_photo(chat_id, message.reply_to_message.photo.file_id, string, ParseMode.HTML)

                        elif message.reply_to_message.voice: #ответ на голосовое сообщение
                            string = f'{message.text}\n<i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_voice(chat_id, message.reply_to_message.voice.file_id, string, ParseMode.HTML)   

                        elif message.reply_to_message.document:
                            if message.reply_to_message.caption:
                                string = f'{message.text}\n{message.reply_to_message.caption} <i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                
                            else:
                                string = f'{message.text}\n<i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'

                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_document(chat_id, message.reply_to_message.document.file_id, caption=string, parse_mode=ParseMode.HTML)  
                        
                        if message.chat.type.name == 'PRIVATE':
                            add_user_task(message.chat.id, message.chat.first_name, message.chat.last_name)
                        elif message.chat.type.name == 'GROUP' or 'SUPERGROUP':
                            add_user_task(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name)


                    else: #если сообщение не является ответом, то берется предыдущее сообщение
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
                        
                        if message.chat.type.name == 'PRIVATE':
                            add_user_task(message.chat.id, message.chat.first_name, message.chat.last_name)
                        elif message.chat.type.name == 'GROUP' or 'SUPERGROUP':
                            add_user_task(previous_message.from_user.id, previous_message.from_user.first_name, previous_message.from_user.last_name)

                    print('Задача сохранена в группе.')
                    

                elif (any(tag in message.text.lower() for tag in tags) and ((any(message.text.lower().split(tag)[-1] == '' for tag in tags)) or any(message.text.lower().split(tag)[-1][0] == '\n' for tag in tags))) or any(tag in message.text.lower() for tag in tags_b): 
                    string = f'{message.text}\n\n____\n{message.from_user.mention} - {date}'
                    if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                        string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                    if message.chat.type.name == 'GROUP':
                        string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)' # если в сообщении есть тэг и какой-то текст
                    if message.chat.type.name == 'PRIVATE':
                        string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                    saved_message = await app.send_message(chat_id, string, ParseMode.HTML, disable_web_page_preview=True)
                    print('Задача сохранена в группе.')
                    
                    if message.chat.type.name == 'PRIVATE':
                        add_user_task(message.chat.id, message.chat.first_name, message.chat.last_name)
                    elif message.chat.type.name == 'GROUP' or 'SUPERGROUP':
                        add_user_task(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
                    


            elif message.photo: # если сообщение есть фото
                if message.caption: # если у фото есть описание
                    if message.caption.lower() in tags: # если в описании только тэг
                        if message.reply_to_message: # если сообщение есть ответ на другое сообщение
                            if message.reply_to_message.text: # если ответное сообщение есть текст
                                string = f'{message.caption}\n{message.reply_to_message.text} <i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_photo(chat_id, message.photo.file_id, string, ParseMode.HTML)
                            
                            elif message.reply_to_message.photo: # ответ на фото
                                if message.reply_to_message.caption: # ответ на фото с описанием
                                    string = f'{message.caption}\n{message.reply_to_message.caption} <i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                
                                else:
                                    string = f'{message.caption}\n\n____\n{message.from_user.mention} - {date}'
                                
                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_photo(chat_id, message.photo.file_id, string, ParseMode.HTML)

                            elif message.reply_to_message.document:
                                if message.reply_to_message.caption:
                                    string = f'{message.caption}\n{message.reply_to_message.caption} <i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                
                                else:
                                    string = f'{message.caption}\n\n____\n{message.from_user.mention} - {date}'

                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_document(chat_id, message.reply_to_message.document.file_id, caption=string, parse_mode=ParseMode.HTML) 
                            
                            if message.chat.type.name == 'PRIVATE':
                                add_user_task(message.chat.id, message.chat.first_name, message.chat.last_name)
                            elif message.chat.type.name == 'GROUP' or 'SUPERGROUP':
                                add_user_task(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name)
                        
                        else: # берется сообщение, стоящее перед тегом
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
                        
                            if message.chat.type.name == 'PRIVATE':
                                add_user_task(message.chat.id, message.chat.first_name, message.chat.last_name)
                            elif message.chat.type.name == 'GROUP' or 'SUPERGROUP':
                                add_user_task(previous_message.from_user.id, previous_message.from_user.first_name, previous_message.from_user.last_name)
                        
                        print('Задача сохранена в группе.')
                        
                    
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
                            
                            if message.chat.type.name == 'PRIVATE':
                                add_user_task(message.chat.id, message.chat.first_name, message.chat.last_name)
                            elif message.chat.type.name == 'GROUP' or 'SUPERGROUP':
                                add_user_task(message.from_user.id, message.from_user.first_name, message.from_user.last_name)


            elif message.document:
                if message.caption: # если у документа есть описание
                    if message.caption.lower() in tags: # если в описании только тэг
                        if message.reply_to_message: # если сообщение есть ответ на другое сообщение
                            if message.reply_to_message.text: # если ответное сообщение есть текст
                                string = f'{message.caption}\n{message.reply_to_message.text} <i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_document(chat_id, message.document.file_id, caption=string, parse_mode=ParseMode.HTML)
                            
                            elif message.reply_to_message.photo: # ответ на фото
                                if message.reply_to_message.caption: # ответ на фото с описанием
                                    string = f'{message.caption}\n{message.reply_to_message.caption} <i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                
                                else:
                                    string = f'{message.caption}\n<i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'

                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_document(chat_id, message.document.file_id, caption=string, parse_mode=ParseMode.HTML)

                            elif message.reply_to_message.document:
                                if message.reply_to_message.caption:
                                    string = f'{message.caption}\n{message.reply_to_message.caption} <i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                else:
                                    string = f'{message.caption}\n<i>{message.reply_to_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                
                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_document(chat_id, message.document.file_id, caption=string, parse_mode=ParseMode.HTML) 
                            if message.chat.type.name == 'PRIVATE':
                                add_user_task(message.chat.id, message.chat.first_name, message.chat.last_name)
                            elif message.chat.type.name == 'GROUP' or 'SUPERGROUP':
                                add_user_task(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name)

                        else: # берется сообщение, стоящее переде тегом
                            async for i in app.get_chat_history(message.chat.id, limit=1, offset_id=message.id):
                                previous_message = i

                            if previous_message.text: # если ответное сообщение есть текст
                                string = f'{message.caption}\n{previous_message.text} <i>{previous_message.from_user.mention}</i>\n\n____\n{message.from_user.mention} - {date}'
                                if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                    string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'GROUP':
                                    string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                                if message.chat.type.name == 'PRIVATE':
                                    string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                                saved_message = await app.send_document(chat_id, message.document.file_id, caption=string, parse_mode=ParseMode.HTML)
                            
                            elif previous_message.photo: # ответ на фото
                                if previous_message.caption: # ответ на фото с описанием
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
                        
                            if message.chat.type.name == 'PRIVATE':
                                add_user_task(message.chat.id, message.chat.first_name, message.chat.last_name)
                            elif message.chat.type.name == 'GROUP' or 'SUPERGROUP':
                                add_user_task(previous_message.from_user.id, previous_message.from_user.first_name, previous_message.from_user.last_name)

                        print('Задача сохранена в группе.')
                        

                    elif (any(tag in message.caption.lower() for tag in tags) and ((any(message.caption.lower().split(tag)[-1] == '' for tag in tags)) or any(message.caption.lower().split(tag)[-1][0] == '\n' for tag in tags))) or any(tag in message.caption.lower() for tag in tags_b):  # если в описании есть тэг и какой-то текст # если в описании есть тэг и какой-то текст
                            string = f'{message.caption}\n\n____\n{message.from_user.mention} - {date}'
                            if message.chat.type.name == 'CHANNEL' or message.chat.type.name == 'SUPERGROUP':
                                string += f' (<a href="{message.link}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'GROUP':
                                string += f' (<a href="https://web.telegram.org/z/#{message.chat.id}">{message.chat.title}</a>)'
                            if message.chat.type.name == 'PRIVATE':
                                string += f' (<a href="https://t.me/{message.chat.username}">{message.chat.first_name}</a>)'
                            saved_message = await app.send_document(chat_id, message.document.file_id, caption=string, parse_mode=ParseMode.HTML)
                            print('Задача сохранена в группе.')

                            if message.chat.type.name == 'PRIVATE':
                                add_user_task(message.chat.id, message.chat.first_name, message.chat.last_name)
                            elif message.chat.type.name == 'GROUP' or 'SUPERGROUP':
                                add_user_task(message.from_user.id, message.from_user.first_name, message.from_user.last_name)

            return saved_message
        except Exception as err:
            print(message.chat.type.name)
            print(err)