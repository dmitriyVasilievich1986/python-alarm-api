from alarm.api.api_server import app
from alarm.variables.server import HOST, PORT
from alarm.websocket.ws import start_server

from threading import Thread
import asyncio


api = Thread(target=app.run, kwargs={"port": PORT, "host": HOST})
api.start()

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
