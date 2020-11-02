import configparser
import datetime
import decimal
import pymysql


from flask import jsonify
from geopy.distance import geodesic

config = configparser.ConfigParser()
config.read("./conf.ini")
mysql = {}
for key in config["mysql"]:
    mysql[key] = eval(config["mysql"][key])


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


def is_in_range(json, longitude, latitude, distance):
    return geodesic((json["latitude"], json["longitude"]), (latitude, longitude)).km <= distance


def is_num(variable):
    return isinstance(variable, int) or isinstance(variable, float)


def is_str(variable):
    return isinstance(variable, str)


def is_dict(variable):
    return isinstance(variable, dict)
