from userbot import app, main
from server import init_web_server

import asyncio
from threading import Thread

Thread(target=asyncio.run, args=(init_web_server(),)).start()
app.run(main())