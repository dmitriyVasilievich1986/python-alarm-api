from ..database.db_class import mysql_database

from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/alarm", methods=["GET", "POST"])
def alarm(*args, **kwargs):
    if request.method == "GET":
        return json.dumps(mysql_database.get_all_alarms())
    elif request.method == "POST":
        data = json.loads(request.data["alarm"])
        mysql_database.insert_new_alarm(
            name=data["name"], description=data["description"], time_stamp=data["time"]
        )
        return "Ok"
    return "Not Ok"

