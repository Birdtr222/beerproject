import datetime

import bcrypt as bcrypt
import jwt
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session

from decorator import login_requried
from setting import SECRET

app = Flask(__name__, template_folder="templates")
# app.config["MONGO_URL"] = "mongodb://localhost:27017/beer"

app.config["DEBUG"] = True
app.secret_key = "1234"


import requests
from bs4 import BeautifulSoup

import pymongo
from pymongo import MongoClient

import json

# ----------DB생성----------
client = pymongo.MongoClient('localhost', 27017)
# client = MongoClient('mongodb://test:test@localhost', 27017)
db = client['TwoFrontFourBack']
db_list = db.list_collection_names()

file_path = "beer.json"
with open(file_path, "r", encoding='UTF-8-sig') as json_file:
    beer_data = json.load(json_file)

if "beer" in db_list:
    print(db['beer'])

else:
    add_data = db['beer'].insert_many(beer_data)

beer_db = db['beer']


# ----------HTML 화면 보여주기----------
@app.route('/')
def home():
    userid = session.get('userid', None)
    return render_template('index.html', userid = userid)


@app.route('/page', methods=['GET'])
def page():
    beers = list(db.beer.find({}, {'_id': False}))
    return jsonify({'all_beers': beers})

# ----------페이지네이션----------
@app.route("/pagelist", methods=['GET'])
def boardlist():

    page = request.args.get('page', 1, type=int)

    print(page)

    limit = 18
    board_list = list(db.beer.find({}, {'_id':False})[limit*(page-1): limit*page])
    print(board_list)

    return jsonify({'all_beers': board_list})


# ----------검색 기능----------
@app.route('/api/search', methods=['GET'])
def search_host():
    name_search = request.args.get('search_name_give')

    beer_search = list(beer_db.find({'맥주 이름': {'$regex': f'.*{name_search}.*'}}, {"_id": False}))
    return jsonify({'beer_search': beer_search})

# ----------회원 가입 구현----------
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == "POST" :
        id = request.form.get("id", type = str)
        pw = request.form.get("pw", type = str)
        pw2 = request.form.get("pw_check", type = str)
        name = request.form.get("name", type = str)

        if name == "" or id == "" or pw == "" or pw2 == "":
            flash("입력되지 않은 값이 있습니다.")
            return render_template("join.html")

        if pw != pw2:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("join.html")

        data = db.users.find_one({"id": id})
        if data is not None:
            flash("이미 존재하는 아이디 입니다.")
            return render_template("join.html")


        byte_pass = pw.encode("utf-8")
        encode_password = bcrypt.hashpw(byte_pass, bcrypt.gensalt())
        print(encode_password)
        decode_password = encode_password.decode("utf-8")
        print(decode_password)

        current_utc_date = datetime.datetime.utcnow()
        doc = {
            "id": id,
            "pw": decode_password,
            "name": name,
            "register_date": current_utc_date,
            "logintime": "",
            "logincount": 0
        }

        db.users.insert_one(doc)
        return render_template('index.html')

    else:
        return render_template("join.html")



# ----------로그인 구현----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        id = request.form.get("id")
        pw = request.form.get("password")
        print(id, pw)


        #id 확인
        data = db.users.find_one({"id": id}, {'_id': False} )
        if data is None:
            # flash("회원 정보가 없습니다")
            return jsonify({"msg": "INVALID_ID"})

        #비밀번호 확인
        if not bcrypt.checkpw(pw.encode("utf-8"), data['pw'].encode("utf-8")):
            flash("비밀번호가 일치하지 않습니다.")
            return jsonify({"msg": "INVALID_PASSWORD"})

        #JWT 토큰 발행
        access_token = jwt.encode({"id": id}, SECRET, algorithm="HS256" )
        session["userid"] = request.form.get('id')
        return jsonify({"msg": "SUCCESS", "access_token": access_token})
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('userid', None)
    flash("로그아웃 되었습니다.")
    return redirect('/')

# ----------좋아요 기능----------
@app.route('/api/like', methods=['POST'])
def like_beer():
    name_receive = request.form['name_give']
    target_star = db.beer.find_one({'맥주 이름': name_receive})
    current_like = target_star['좋아요']

    new_like = current_like + 1

    db.beer.update_one({'맥주 이름': name_receive}, {'$set': {'좋아요': new_like}})

    return jsonify({'msg': '당신이 좋아하는 맥주!'})


# -----국가 소분류 필터링----------

@app.route('/domestic', methods=['GET'])
def domestic():
    page = request.args.get('page', 2, type=int)


    limit = 18
    korean_beers = list(db.beer.find({'국가 소분류': '대한민국'}, {'_id': False}))
    return jsonify({'all_korean_beers': korean_beers})


@app.route('/income', methods=['GET'])
def income():
    page = request.args.get('page', 2, type=int)

    limit = 18
    imported_beers = list(db.beer.find({'$nor': [{'국가 소분류': {'$regex': '대한민국'}}]}, {'_id': False}))
    return jsonify({'all_imported_beers': imported_beers})


# ---------대분류 필터링-------------
@app.route('/apa', methods=['GET'])
def apa():
    apas = list(db.beer.find({'대분류': 'APA'}, {'_id': False}))
    return jsonify({'all_apa': apas})


@app.route('/ipa', methods=['GET'])
def ipa():
    ipas = list(db.beer.find({'대분류': 'IPA'}, {'_id': False}))
    return jsonify({'all_ipa': ipas})


@app.route('/lager', methods=['GET'])
def lager():
    lagers = list(db.beer.find({'대분류': '라거'}, {'_id': False}))
    return jsonify({'all_lager': lagers})


@app.route('/radler', methods=['GET'])
def radler():
    radlers = list(db.beer.find({'대분류': '라들러'}, {'_id': False}))
    return jsonify({'all_radler': radlers})


@app.route('/wheetBeer', methods=['GET'])
def wheetBeer():
    wheetBeers = list(db.beer.find({'$or': [{'대분류': '밀맥주'}, {'대분류': '윗비어'}]}, {'_id': False}))
    return jsonify({'all_wheetBeers': wheetBeers})


@app.route('/weizen', methods=['GET'])
def weizen():
    weizens = list(db.beer.find({'대분류': '바이젠'}, {'_id': False}))
    return jsonify({'all_weizen': weizens})


@app.route('/cider', methods=['GET'])
def cider():
    ciders = list(db.beer.find({'대분류': '사이더'}, {'_id': False}))
    return jsonify({'all_cider': ciders})


@app.route('/stout', methods=['GET'])
def stout():
    stouts = list(db.beer.find({'대분류': '스타우트'}, {'_id': False}))
    return jsonify({'all_stout': stouts})


@app.route('/ale', methods=['GET'])
def ale():
    ales = list(db.beer.find({'대분류': '에일'}, {'_id': False}))
    return jsonify({'all_ale': ales})


@app.route('/pilsner', methods=['GET'])
def pilsner():
    pilsners = list(db.beer.find({'대분류': '필스너'}, {'_id': False}))
    return jsonify({'all_pilsner': pilsners})


@app.route('/darkBeer', methods=['GET'])
def darkBeer():
    darkBeers = list(db.beer.find({'대분류': '흑맥주'}, {'_id': False}))
    return jsonify({'all_darkBeer': darkBeers})


# ---------도수 필터링----------
@app.route('/degree2', methods=['GET'])
def degree2():
    degree2s = list(db.beer.find({'도수': {'$gte': '2.0%', '$lte': '2.9%'}}, {'_id': False}))
    return jsonify({'all_degree2': degree2s})


@app.route('/degree3', methods=['GET'])
def degree3():
    degree3s = list(db.beer.find({'도수': {'$gte': '3.0%', '$lte': '3.9%'}}, {'_id': False}))
    return jsonify({'all_degree3': degree3s})


@app.route('/degree4', methods=['GET'])
def degree4():
    degree4s = list(db.beer.find({'도수': {'$gte': '4.0%', '$lte': '4.9%'}}, {'_id': False}))
    return jsonify({'all_degree4': degree4s})


@app.route('/degree5', methods=['GET'])
def degree5():
    degree5s = list(db.beer.find({'도수': {'$gte': '5.0%', '$lte': '5.9%'}}, {'_id': False}))
    return jsonify({'all_degree5': degree5s})


@app.route('/degree6', methods=['GET'])
def degree6():
    degree6s = list(db.beer.find({'도수': {'$gte': '6.0%', '$lte': '6.9%'}}, {'_id': False}))
    return jsonify({'all_degree6': degree6s})


@app.route('/degree7', methods=['GET'])
def degree7():
    degree7s = list(db.beer.find({'도수': {'$gte': '7.0%', '$lte': '7.9%'}}, {'_id': False}))
    return jsonify({'all_degree7': degree7s})


@app.route('/degree8', methods=['GET'])
def degree8():
    degree8s = list(db.beer.find({'도수': {'$gte': '8.0%', '$lte': '8.9%'}}, {'_id': False}))
    return jsonify({'all_degre8': degree8s})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
