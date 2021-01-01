# -*- coding: utf-8 -*-
"""
Clask: a http client based on requests just like Flask

"""

from __future__ import print_function, absolute_import, unicode_literals

import requests

from .logger import logger
from .utils import UrlTemplate


class Clask(object):

    def __init__(self, base_url, method="GET",
                 params=None, data=None, query=None, json=None,
                 headers=None, cookies=None, files=None,
                 auth=None, timeout=None, allow_redirects=None, proxies=None,
                 hooks=None, stream=None, verify=None, cert=None):
        """
        支持的参数列表：

        :param base_url: 基本路径
        :param method: 请求方法 GET, OPTIONS, HEAD, POST, PUT, PATCH, DELETE.
        :param params: 路径参数
        :param data:
        :param query: 查询参数
        :param json:
        :param headers:
        :param cookies:
        :param files:
        :param auth:
        :param timeout:
        :param allow_redirects:
        :param proxies:
        :param hooks:
        :param stream:
        :param verify:
        :param cert:
        """

        self.options = {
            'base_url': base_url,
            'method': method,
            'query': query,
            'params': params,
            'data': data,
            'json': json,
            'headers': headers,
            'cookies': cookies,
            'files': files,
            'auth': auth,
            'timeout': timeout,
            'allow_redirects': allow_redirects,
            'proxies': proxies,
            'hooks': hooks,
            'stream': stream,
            'verify': verify,
            'cert': cert,
        }

        self._before_request = None
        self._after_request = None
        self._error_handler = None

    def before_request(self, func):
        """
        注册请求前处理器
        @api.before_request
        def before_request(**kwargs):
            return kwargs

        """
        self._before_request = func

    def after_request(self, func):
        """
        @api.after_request
        def after_request(response):
            return response

        response: {
        'apparent_encoding', 'close', 'connection',
        'content', 'cookies', 'elapsed', 'encoding',
        'headers', 'history', next, history, is_permanent_redirect,
        links,iter_content, is_redirect, iter_lines, json,
        ok, raise_for_status, url, status_code, text,
        request, reason, raw
        }
        """
        self._after_request = func

    def error_handler(self, func):
        """
        @api.error_handler
        def error_handler(e):
            pass
        """
        self._error_handler = func

    def process_url_params(self, url, params):
        """url 路径参数替换"""
        return UrlTemplate(url).substitute(**params)

    def process_request(self, url, **kwargs):

        # 参数合并
        kwargs = {**self.options, **kwargs, 'url': url}

        # 过滤无效参数
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        # 请求前参数处理
        if self._before_request:
            kwargs = self._before_request(**kwargs)

        logger.debug(kwargs)

        # url拼接
        full_url = kwargs.pop('base_url') + kwargs.pop('url')

        # 处理路径参数
        if 'params' in kwargs:
            full_url = self.process_url_params(url=full_url, params=kwargs.pop("params"))

        logger.debug(full_url)

        # 交换参数为requests 正常参数
        if 'query' in kwargs:
            kwargs['params'] = kwargs.pop("query")

        try:
            response = requests.request(url=full_url, **kwargs)

        except Exception as e:
            # 异常处理
            if self._error_handler:
                return self._error_handler(e)
            else:
                raise e

        # 请求后响应处理
        if self._after_request:
            response = self._after_request(response)

        return response

    def request(self, url=None, method="GET", **options):

        def decorator(func):
            def inner(*args, **kwargs):
                _url = url or func.__name__

                # 参数预处理
                result = func(*args, **kwargs)
                if result:
                    kwargs = result

                kwargs = {**options, 'method': method, 'url': _url, **kwargs}

                return self.process_request(**kwargs)

            return inner

        return decorator

    def get(self, url, **options):
        return self.request(url, method='GET', **options)

    def post(self, url, **options):
        return self.request(url, method='POST', **options)

    def delete(self, url, **options):
        return self.request(url, method='DELETE', **options)

    def options(self, url, **options):
        return self.request(url, method='OPTIONS', **options)

    def head(self, url, **options):
        return self.request(url, method='HEAD', **options)

    def put(self, url, **options):
        return self.request(url, method='PUT', **options)

    def patch(self, url, **options):
        return self.request(url, method='PATCH', **options)
