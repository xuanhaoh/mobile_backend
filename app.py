import random

from flask import Flask, request
from pymysql import IntegrityError

from utils import *

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "mobile backend"


@app.route("/init", methods=["GET"])
def init():
    connection = pymysql.connect(**{k: v for k, v in mysql.items() if k != "db"})
    try:
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS mobile")

            cursor.execute("SELECT * FROM information_schema.SCHEMATA  WHERE SCHEMA_NAME = 'mobile'")
            result = cursor.fetchall()
            if not result:
                cursor.execute("CREATE DATABASE IF NOT EXISTS mobile")
                cursor.execute("USE mobile")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS USER(
                    user_id INT NOT NULL AUTO_INCREMENT,
                    username VARCHAR(20) NOT NULL unique,
                    longitude DECIMAL(10,6) NOT NULL,
                    latitude DECIMAL(10,6) NOT NULL,
                    creation_date DATE NOT NULL,
                    PRIMARY KEY ( user_id )
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS RECORD(
                    grade_id INT NOT NULL AUTO_INCREMENT,
                    username VARCHAR(20) NOT NULL,
                    grade INT NOT NULL,
                    creation_date DATE NOT NULL,
                    PRIMARY KEY ( grade_id )
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                """)
        return "Success"
    finally:
        connection.close()


@app.route("/add/random_data", methods=["GET"])
def random_data():
    connection = pymysql.connect(**mysql)
    try:
        with connection.cursor() as cursor:
            for i in range(10):
                username = "user" + str(i+1)
                longitude = random.randrange(-180, 180)
                latitude = random.randrange(-90, 90)
                cursor.execute("""
                                INSERT INTO USER (username, longitude, latitude, creation_date)
                                VALUES ('{}', '{}', '{}', CURDATE())
                            """.format(username, longitude, latitude))
            for i in range(20):
                username = "user" + str(random.randint(1, 10))
                grade = random.randrange(0, 100)
                cursor.execute("""
                                INSERT INTO RECORD (username, grade, creation_date)
                                VALUES ('{}', '{}', CURDATE())
                            """.format(username, grade))
        connection.commit()
        return "Success"
    except Exception as e:
        print(e)
        return "Unknown error", "500"
    finally:
        connection.close()


@app.route("/add/user", methods=["POST"])
def add_user():
    connection = pymysql.connect(**mysql)
    try:
        if request.form and is_dict(request.form):
            username = request.form["username"]
            longitude = request.form["longitude"]
            latitude = request.form["latitude"]
        elif request.json and is_dict(request.json):
            username = request.json["username"]
            longitude = request.json["longitude"]
            latitude = request.json["latitude"]
        else:
            return "Empty request", "400"
        if not (is_str(username) and is_num(longitude) and is_num(latitude)):
            return "Wrong format", "400"
        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            return "Longitude not in [-180, 180] or latitude not in [-90, 90]", "400"
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


@app.route("/add/record", methods=["POST"])
def add_record():
    connection = pymysql.connect(**mysql)
    try:
        if request.form and is_dict(request.form):
            username = request.form["username"]
            grade = request.form["grade"]
        elif request.json and is_dict(request.json):
            username = request.json["username"]
            grade = request.json["grade"]
        else:
            return "Empty request", "400"
        if not (is_str(username) and is_num(grade)):
            return "Wrong format", "400"
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


@app.route("/update/user", methods=["POST"])
def update_user():
    connection = pymysql.connect(**mysql)
    try:
        if request.form and is_dict(request.form):
            username = request.form["username"]
            longitude = request.form["longitude"]
            latitude = request.form["latitude"]
        elif request.json and is_dict(request.json):
            username = request.json["username"]
            longitude = request.json["longitude"]
            latitude = request.json["latitude"]
        else:
            return "Empty request", "400"
        if not (is_str(username) and is_num(longitude) and is_num(latitude)):
            return "Wrong format", "400"
        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            return "Longitude not in [-180, 180] or latitude not in [-90, 90]", "400"
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE USER
                SET
                    longitude = {},
                    latitude = {}
                WHERE username = '{}'
            """.format(longitude, latitude, username))
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


@app.route("/query/nearby_record", methods=["POST"])
def query_nearby_record():
    connection = pymysql.connect(**mysql)
    try:
        if request.form and is_dict(request.form):
            longitude = request.form["longitude"]
            latitude = request.form["latitude"]
            distance = request.form["distance"]
        elif request.json and is_dict(request.json):
            longitude = request.json["longitude"]
            latitude = request.json["latitude"]
            distance = request.json["distance"]
        else:
            return "Empty request", "400"
        if not (is_num(longitude) and is_num(latitude) and is_num(distance)):
            return "Wrong format", "400"
        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            return "Longitude not in [-180, 180] or latitude not in [-90, 90]", "400"
        with connection.cursor() as cursor:
            cursor.execute("""SELECT USER.username as username, longitude, latitude, grade
                FROM USER JOIN (SELECT username, MAX(grade) as grade
                    FROM (SELECT username, grade FROM RECORD ORDER BY grade DESC) as a
                    GROUP BY username) as b
                ON USER.username = b.username""")
            result = cursor.fetchall()
        result = [i for i in result if is_in_range(i, longitude, latitude, distance)]
        return to_json(result)
    except Exception as e:
        print(e)
        return "Unknown error", "500"
    finally:
        connection.close()


@app.route("/query/leaderboard", methods=["GET"])
def query_leaderboard():
    connection = pymysql.connect(**mysql)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT *
                              FROM (SELECT username, MAX(grade) as grade, MAX(creation_date) as creation_date
                                    FROM (SELECT username, grade, creation_date
                                          FROM RECORD
                                          ORDER BY grade DESC) as a
                                    GROUP BY username) as b
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
    app.run(host="0.0.0.0", port=5000, debug=True)
