from ..database.db_class import mysql_database
from ..variables.websocket import PORT, HOST

import websockets
import asyncio
from datetime import datetime
import json


async def index(websocket, path):
    """проверяем будильники и при срабатывании отправляем сообщение,
    удаляем будильник из БД
    """
    for x in mysql_database.get_all_alarms():
        if datetime.now() >= datetime.strptime(x["time"], "%Y-%m-%d %H:%M"):
            await websocket.send(json.dumps(x))
            mysql_database.delete_alarm(x["id"])


start_server = websockets.serve(index, HOST, PORT)
