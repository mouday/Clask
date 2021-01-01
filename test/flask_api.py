# -*- coding: utf-8 -*-

import random

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/get")
def get():
    """通过get方式传递查询参数"""
    name = request.args.get("name")
    age = random.randint(10, 30)

    data = {
        "name": name,
        "age": age,
    }

    return jsonify(data)


@app.route("/student/<uid>/<name>")
def getStudent(uid, name):
    """通过get方式传递查询参数"""
    data = {
        "name": name,
        "uid": uid,
    }

    return jsonify(data)


@app.route("/post", methods=['POST'])
def post():
    """通过post方式提交json数据"""
    name = request.json.get("name")
    age = random.randint(10, 30)

    data = {
        "name": name,
        "age": age,
    }

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
