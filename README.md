# Clask

## 简介
Clask: a http client based on requests just like Flask

对比：

| - | 描述 | 运行环境 |
| - | - | - | 
| Flask | 路由映射到方法 | 服务端 |
| Clask | 方法映射到路由 | 客户端 |
 
## 安装
```bash
pip install clask
```

## 使用示例

1、Flask作为服务器代码
```python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/get")
def get():

    data = {
        "name": "Tom",
        "age":23
    }

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

```

2、Clask作为客户端的代码

```python
# -*- coding: utf-8 -*-

from clask import Clask

api = Clask(base_url="http://127.0.0.1:5000")


# 发送get请求
@api.request("/get")
def get():
    pass


if __name__ == '__main__':
    get()
    # '{"name": "Tom", "age": 23}'
```

