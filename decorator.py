from functools import wraps
import jwt
from bson import ObjectId
from flask import Flask, render_template, jsonify, request
from setting import SECRET
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['TwoFrontFourBack']


def login_requried(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        try:
            access_token = request.headers.get("Authorization")
            print(access_token)

            if access_token:
                token_payload = jwt.decode(access_token, SECRET, algorithms="HS256")

                id = ObjectId(token_payload['id'])
                name = db.users.find_one({"_id": id})
                request.name = name

                return func(*args, **kwargs)

            return jsonify({"msg": "need_login"})

        except jwt.DecodeError:
            return jsonify({"msg": "need_login"})

    return decorated_func