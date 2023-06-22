import sqlite3
from datetime import datetime, timedelta, date

from config.config import offset


offset = timedelta(hours=offset+3)
date_data = {'Mon': 'Пн', 'Tue': 'Вт', 'Wed': 'Ср', 'Thu': 'Чт', 'Fri': 'Пт', 'Sat': 'Сб', 'Sun': 'Вс', '01':'Январь', '02': 'Февраль', '03': 'Март', '04': 'Апрель', '05': 'Май', '06': 'Июнь', '07': 'Июль', '08': 'Август', '09': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}

def get_everyday_message():
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM day_time_data where type = 'completed_tasks'")
    completed_tasks = sum(int(i) for i in cursor.fetchall()[0][1:])
    cursor.execute("SELECT * FROM day_time_data where type = 'tasks'")
    all_tasks = sum(int(i) for i in cursor.fetchall()[0][1:])
    effectiveness = int(completed_tasks*100 / all_tasks if all_tasks != 0 else completed_tasks*100)
    cursor.execute("SELECT info FROM day_effectiveness")
    yestarday_effectiveness = int(cursor.fetchall()[0][0])
    cursor.execute(f"UPDATE day_effectiveness SET info = {effectiveness}")
    connection.commit()
    comparison = round(effectiveness - yestarday_effectiveness)
    if effectiveness >= 100: 
        emodji = '\U0001F49A'
    elif effectiveness >= 50:
        emodji = '\U0001F49B'
    else:
        emodji = '\U00002764'
    if comparison > 10:
        string_2 = f"На {comparison}% лучше, чем вчера. **Красавчик**\U0001F4AA"
    elif comparison < -10:
        string_2 = f"На {abs(comparison)}% хуже, чем вчера. **Завтра постарайся**\U0001F609"
    else:
        string_2 = f"Также круто, как и вчера! **Браво!**\U0001F44F"
    string = f"За день выполненно {completed_tasks} задач из {all_tasks}.\n{emodji} Эффективность дня - **{effectiveness}%**\n\n{string_2}"
    connection.close()
    everyday_job()
    return string

def get_everyweek_message():
    key = datetime.now()+offset
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM completed_tasks where id = 1")
    completed_tasks = cursor.fetchall()[0][0]
    cursor.execute("SELECT week FROM tasks_set")
    all_tasks = sum(sum(cursor.fetchall(), ()))
    all_tasks = 1 if all_tasks == 0 else all_tasks
    effectiveness = round(completed_tasks*100 / all_tasks)
    if effectiveness > 100: 
        emodji = '\U0001F49A'
    elif effectiveness > 50:
        emodji = '\U0001F49B'
    else:
        emodji = '\U00002764'
    string = f"За неделю выполненно {completed_tasks} задач из {all_tasks}.\n{emodji} Общая эффективность - **{effectiveness}%**"
    cursor.execute(f"UPDATE tasks_set SET week = 0")
    connection.commit()
    cursor.execute("UPDATE completed_tasks SET week = 0")
    connection.commit()
    for i in range(0, 8):
        cursor.execute(f"UPDATE week_time_data SET '{(key+timedelta(days=i)).strftime('%a')}' = 0")
    connection.commit()
    connection.close()
    return string

def everyday_job():
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute("SELECT day FROM tasks_set")
    hour_tasks_count = sum(sum(cursor.fetchall(), ()))
    cursor.execute("SELECT day FROM completed_tasks")
    hour_complited_tasks_count = sum(sum(cursor.fetchall(), ()))
    key = (datetime.now()+offset).strftime('%d.%m')
    week_day_key = (datetime.now()+offset).strftime('%a')
    hour_key = datetime.now()+offset
    try:
        cursor.execute(f"ALTER TABLE month_time_data ADD COLUMN '{key}' text")
    except: pass
    cursor.execute(f"UPDATE month_time_data SET '{key}' = '{hour_tasks_count}' where type = 'tasks'")
    connection.commit()
    cursor.execute(f"UPDATE month_time_data SET '{key}' = '{hour_complited_tasks_count}' where type = 'completed_tasks'")
    connection.commit()
    cursor.execute(f"UPDATE week_time_data SET '{week_day_key}' = '{hour_tasks_count}' where type = 'tasks'")
    connection.commit()
    cursor.execute(f"UPDATE week_time_data SET '{week_day_key}' = '{hour_complited_tasks_count}' where type = 'completed_tasks'")
    connection.commit()
    for i in range(0, 25):
        cursor.execute(f"UPDATE day_time_data SET '{(hour_key+timedelta(hours=i)).strftime('%H:00')}' = 0")
        connection.commit()
    cursor.execute("UPDATE tasks_set SET day = 0")
    connection.commit()
    cursor.execute("UPDATE completed_tasks SET day = 0")
    connection.commit()
    connection.close()


def everyhour_job():
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute("SELECT hour FROM tasks_set")
    hour_tasks_count = sum(sum(cursor.fetchall(), ()))
    cursor.execute("SELECT hour FROM completed_tasks")
    hour_complited_tasks_count = sum(sum(cursor.fetchall(), ()))
    key = (datetime.now()+offset).strftime('%H:00')
    cursor.execute(f"UPDATE day_time_data SET '{key}' = '{hour_tasks_count}' where type = 'tasks'")
    connection.commit()
    cursor.execute(f"UPDATE day_time_data SET '{key}' = '{hour_complited_tasks_count}' where type = 'completed_tasks'")
    connection.commit()
    cursor.execute("UPDATE tasks_set SET hour = 0")
    connection.commit()
    cursor.execute("UPDATE completed_tasks SET hour = 0")
    connection.commit()
    connection.close()


def add_completed_task():
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE completed_tasks SET hour = hour+1, day = day+1, week = week+1, month = month+1, year = year + 1 where id = 1")
    connection.commit()
    connection.close()


def add_user_task(user_id, first_name, last_name):
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tasks_set')
    keys = (string[0] for string in cursor.fetchall())
    if str(user_id) in keys:
        cursor.execute(f"UPDATE tasks_set SET hour = hour+1, day = day+1, week = week+1, month = month+1, year = year + 1 where id = '{user_id}'")
    else:
        cursor.execute(F"INSERT INTO tasks_set VALUES('{user_id}', '{first_name}', '{last_name}', 1, 1, 1, 1, 1)")
    connection.commit()
    connection.close()


def get_name_tasks(period):
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT first_name, last_name, {period} FROM tasks_set')
    keys = cursor.fetchall()
    keys.sort(key=lambda keys: keys[2], reverse=True)
    return {"response":keys}

def get_year_tasks(tasks_type):
    month = ''
    month_count = 0
    data_dict = dict()
    connection = sqlite3.connect("mydatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM month_time_data where type='{tasks_type}'")
    data = dict(cursor.fetchall()[0])
    del data['type']
    connection.close()
    for i in data.keys():
        if date_data[i.split('.')[-1]] == month:
            month_count+=int(data[i])
            data_dict[month] = month_count
            continue
        month = date_data[i.split('.')[-1]]
        month_count = int(data[i])
        data_dict[month] = month_count
    connection.close()

    return {'response': data_dict}


def get_month_tasks(tasks_type):
    data_dict = dict()
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM month_time_data where type='{tasks_type}'")
    try:
        data = cursor.fetchall()[0][1:][-31:]
    except IndexError:
        data = cursor.fetchall()[0][1:]
    connection.close()
    last_datetime = date.today() - timedelta(days=len(data))
    for i in data:
        last_datetime+=timedelta(days=1)
        if i is not None:
            data_dict[last_datetime.strftime('%d.%m')] = i
        else:
            data_dict[last_datetime.strftime('%d.%m')] = 0

    return {'response': data_dict}

def get_week_tasks(tasks_type):
    t=0
    data_dict = dict()
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM week_time_data where type='{tasks_type}'")
    data = cursor.fetchall()[0][1:]
    connection.close()
    for i in data:
        data_dict[date_data[(date(year=2023, month=1, day=23) + timedelta(days=t)).strftime('%a')]] = i
        t+=1
    return {'response': data_dict}

def get_day_task(tasks_type):
    t=0
    data_dict = dict()
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM day_time_data where type='{tasks_type}'")
    data = cursor.fetchall()[0][1:]
    connection.close()
    for i in data:
        data_dict[str(timedelta(hours=t))[0:-3]] = i
        t+=1
    return {'response': data_dict}

def create_database():
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE day_effectiveness(id integer PRIMARY KEY, info text)")
    connection.commit()
    connection.close()


if __name__ == '__main__':
    pass
    #create_database()