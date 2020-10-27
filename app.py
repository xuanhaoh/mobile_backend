from flask import Flask, request
from pymysql import IntegrityError
from werkzeug.exceptions import BadRequestKeyError

from utils import *

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "mobile backend"


@app.route("/user/add", methods=["POST"])
def add_user():
    connection = pymysql.connect(**mysql)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO USER (username, password, creation_date)
                VALUES ('{}', '{}', CURDATE())
            """.format(request.form["username"], request.form["password"]))
        connection.commit()
        return "Success", "200"
    except IntegrityError:
        return "Duplicate username", "400"
    except BadRequestKeyError:
        return "Username and password required", "400"
    finally:
        connection.close()


@app.route("/record/add", methods=["POST"])
def add_record():
    connection = pymysql.connect(**mysql)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO RECORD (username, grade, longitude, latitude, creation_date)
                VALUES ('{}', '{}', '{}', '{}', CURDATE())
            """.format(request.form["username"], request.form["grade"], request.form["longitude"],
                       request.form["latitude"]))
        connection.commit()
        return "Success", "200"
    except BadRequestKeyError:
        return "Username, grade and position required", "400"
    finally:
        connection.close()


@app.route("/user/query", methods=["GET"])
def query_user():
    connection = pymysql.connect(**mysql)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM USER")
            result = cursor.fetchall()
        return to_json(result)
    finally:
        connection.close()


@app.route("/record/query", methods=["GET"])
def query_record():
    connection = pymysql.connect(**mysql)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM RECORD")
            result = cursor.fetchall()
        return to_json(result)
    finally:
        connection.close()


@app.route("/user/login", methods=["POST"])
def login_user():
    connection = pymysql.connect(**mysql)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM USER WHERE username = '{}' AND password = '{}'
            """.format(request.form["username"], request.form["password"]))
            result = cursor.fetchall()
        if result:
            return "Success", "200"
        else:
            return "Incorrect username or password", "400"
    finally:
        connection.close()


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=5000, debug=True)
