# -*- coding: utf-8 -*-
from clask import Clask

api = Clask(base_url="http://127.0.0.1:5000")


# 发送get请求
@api.route("/get")
def get(args):
    pass


# 发送post请求
@api.route("/post", method="POST")
def post1(json):
    pass


# 使用post方法
@api.post("/post")
def post2(json):
    pass


# 加入查询参数，自定义接口参数名
@api.route("/student/{uid}/{name}")
def getStudent1(uid, name):
    return {
        "args": {
            "uid": uid,
            "name": name
        }
    }


# 等价于：只是调用函数传入参数不一样
@api.route("/student/{uid}/{name}")
def getStudent1(params):
    pass


# 前置处理器
@api.before_request
def before_request(kwargs):
    print('before_request::', kwargs)
    return kwargs


# 后置处理器
@api.after_request
def after_request(response):
    print('after_request', response.status_code)
    return response.json()


# 异常处理器
@api.error_handler
def error_handler(e):
    print(e)
