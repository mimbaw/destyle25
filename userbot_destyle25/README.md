api_id, api_hash, токен бота, эмодзи выполненного задания и чат, куда пересылаются сообщения 
указываете в файле "config.py" в папке config. Особое внимание обратит на последний пункт, нужно указывать именно id, цифрами.
Пример файла "config.py":


token = "123456:jnvjrtghntgefewf4wefwgfh"
api_id = "12345678"
api_hash = "123a45b67cde891f23ghi456j78k9123"
chat_id = 213244234
OK_SIGN = '👌'


Бот запускается файлом main.py. Все, что нужно менять пользователю, находится в файле "config.py"
Библиотеки:
-aiogram
-pyrogram
-sqlite