import configparser
import datetime
import decimal
import random

import pymysql
from flask import jsonify

config = configparser.ConfigParser()
config.read("./conf.ini")
mysql = {}
for key in config["mysql"]:
    mysql[key] = eval(config["mysql"][key])


def init():
    connection = pymysql.connect(**{k: v for k, v in mysql.items() if k != "db"})
    try:
        with connection.cursor() as cursor:
            # for test
            # cursor.execute("DROP DATABASE IF EXISTS mobile")

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

            # for test
            # for i in range(10):
            #     username = "user" + str(i+1)
            #     longitude = random.randrange(-100, 100)
            #     latitude = random.randrange(-100, 100)
            #     cursor.execute("""
            #                     INSERT INTO USER (username, longitude, latitude, creation_date)
            #                     VALUES ('{}', '{}', '{}', CURDATE())
            #                 """.format(username, longitude, latitude))
            # for i in range(20):
            #     username = "user" + str(random.randint(1, 10))
            #     grade = random.randrange(0, 100)
            #     cursor.execute("""
            #                     INSERT INTO RECORD (username, grade, creation_date)
            #                     VALUES ('{}', '{}', CURDATE())
            #                 """.format(username, grade))
            # connection.commit()

    finally:
        connection.close()


def to_json(result):
    items = []
    for item in result:
        items.append({k: parse(v) for k, v in item.items()})
    return jsonify(items)


def parse(obj):
    if isinstance(obj, int) or isinstance(obj, str):
        return obj
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, datetime.date):
        return obj.strftime("%d %b %Y")
