import asyncio
from aiohttp import web
import json

from db import get_name_tasks, get_year_tasks, get_month_tasks,  get_week_tasks, get_day_task

routes = web.RouteTableDef()


@routes.post('/')
async def hello(request: web.Request):
    data = await request.text()
    if "name" in data:
        if "day" in data:
            response = json.dumps(get_name_tasks('day'))
            return web.Response(body=response)
        elif "week" in data:
            response = json.dumps(get_name_tasks('week'))
            return web.Response(body=response)    
        elif "month" in data:
            response = json.dumps(get_name_tasks('month'))
            return web.Response(body=response)    
        elif "year" in data:
            response = json.dumps(get_name_tasks('year'))
            return web.Response(body=response)    
    elif "time" in data:
        if "day" in data:
            response = json.dumps(get_day_task('tasks'))
            return web.Response(body=response)
        elif "week" in data:
            response = json.dumps(get_week_tasks('tasks'))
            return web.Response(body=response)    
        elif "month" in data:
            response = json.dumps(get_month_tasks('tasks'))
            return web.Response(body=response)    
        elif "year" in data:
            response = json.dumps(get_year_tasks('tasks'))
            return web.Response(body=response)   
    elif "decision" in data:
        if "day" in data:
            response = json.dumps(get_day_task('completed_tasks'))
            return web.Response(body=response)
        elif "week" in data:
            response = json.dumps(get_week_tasks('completed_tasks'))
            return web.Response(body=response)    
        elif "month" in data:
            response = json.dumps(get_month_tasks('completed_tasks'))
            return web.Response(body=response)    
        elif "year" in data:
            response = json.dumps(get_year_tasks('completed_tasks'))
            return web.Response(body=response)  

async def init_web_server():
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app, access_log=None)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    while True:
        await asyncio.sleep(10)