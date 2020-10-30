from flask import Flask, request
from pymysql import IntegrityError

from utils import *

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "mobile backend", "400"


@app.route("/user/add", methods=["POST"])
def add_user():
    connection = pymysql.connect(**mysql)
    try:
        if request.form and isinstance(request.form, dict):
            username = request.form["username"]
            longitude = request.form["longitude"]
            latitude = request.form["latitude"]
        elif request.json and isinstance(request.json, dict):
            username = request.json["username"]
            longitude = request.json["longitude"]
            latitude = request.json["latitude"]
        else:
            return "Empty request", "400"
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO USER (username, longitude, latitude, creation_date)
                VALUES ('{}', '{}', '{}', CURDATE())
            """.format(username, longitude, latitude))
        connection.commit()
        return "Success"
    except KeyError:
        return "Username, longitude and latitude required", "400"
    except IntegrityError:
        return "Duplicate username", "400"
    except Exception as e:
        print(e)
        return "Unknown error", "500"
    finally:
        connection.close()


@app.route("/record/add", methods=["POST"])
def add_record():
    connection = pymysql.connect(**mysql)
    try:
        if request.form and isinstance(request.form, dict):
            username = request.form["username"]
            grade = request.form["grade"]
        elif request.json and isinstance(request.json, dict):
            username = request.json["username"]
            grade = request.json["grade"]
        else:
            return "Empty request", "400"
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO RECORD (username, grade, creation_date)
                VALUES ('{}', '{}', CURDATE())
            """.format(username, grade))
        connection.commit()
        return "Success"
    except KeyError:
        return "Username and grade required", "400"
    except Exception as e:
        print(e)
        return "Unknown error", "500"
    finally:
        connection.close()


@app.route("/user/query", methods=["GET"])
def query_user():
    connection = pymysql.connect(**mysql)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username, longitude, latitude, creation_date FROM USER")
            result = cursor.fetchall()
        return to_json(result)
    except Exception as e:
        print(e)
        return "Unknown error", "500"
    finally:
        connection.close()


@app.route("/record/query", methods=["GET"])
def query_record():
    connection = pymysql.connect(**mysql)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT username, grade, creation_date FROM RECORD
                ORDER BY grade DESC
                LIMIT 10""")
            result = cursor.fetchall()
        return to_json(result)
    except Exception as e:
        print(e)
        return "Unknown error", "500"
    finally:
        connection.close()


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=5000, debug=True)
