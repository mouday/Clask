# -*- coding: utf-8 -*-
"""
Clask: a http client based on requests just like Flask

"""

from __future__ import print_function, absolute_import, unicode_literals

import requests

from .logger import logger
from .utils import UrlTemplate
from functools import wraps


class ClaskHandler(object):

    @staticmethod
    def url_join_handler(options):
        """拼接url"""
        options['url'] = options.pop('base_url') + options['url']
        return options

    @staticmethod
    def url_args_handler(options):
        """url 路径参数替换"""
        if 'args' in options:
            options['url'] = UrlTemplate(options['url']).substitute(**options.pop("args"))

        return options

    @staticmethod
    def filter_invalid_handler(options):
        """过滤无效参数"""
        return {k: v for k, v in options.items() if v is not None}


class Clask(object):
    # 默认的请求处理器，放在用户自定义方法之后按顺序执行
    default_before_requests = [
        ClaskHandler.filter_invalid_handler,
        ClaskHandler.url_join_handler,
        ClaskHandler.url_args_handler,
    ]

    def __init__(self, base_url=None, method="GET",
                 params=None, data=None, args=None, json=None,
                 headers=None, cookies=None, files=None,
                 auth=None, timeout=None, allow_redirects=None, proxies=None,
                 hooks=None, stream=None, verify=None, cert=None):
        """
        支持的参数列表：

        :param base_url: 基本路径
        :param method:   请求方法 GET, OPTIONS, HEAD, POST, PUT, PATCH, DELETE.
        :param params:   查询参数 ?name=Tom
        :param data:     formData name=Tom
        :param args:     路径参数 /user/{id}
        :param json:     json {"name": "Tom"}
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
            'args': args,
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

        self._before_requests = []
        self._after_requests = []
        self._error_handler = None

    def before_request(self, func):
        """
        注册请求前处理器
        @api.before_request
        def before_request(options):
            return options

        options 同 self.options
        """
        self._before_requests.append(func)

    def after_request(self, func):
        """
        @api.after_request
        def after_request(response):
            return result

        response: {
            apparent_encoding,
            close,
            connection,
            content,
            cookies,
            elapsed,
            encoding,
            headers,
            history,
            next,
            history,
            is_permanent_redirect,
            links,
            iter_content,
            is_redirect,
            iter_lines,
            json,
            ok,
            raise_for_status,
            url,
            status_code,
            text,
            request,
            reason,
            raw
        }
        """
        self._after_requests.append(func)

    def error_handler(self, func):
        """
        @api.error_handler
        def error_handler(e):
            return result
        """
        self._error_handler = func

    def request(self, url, **kwargs):

        # 参数合并
        options = {**self.options, **kwargs, 'url': url}

        # 请求前参数处理
        for before_request in [*self._before_requests, *self.default_before_requests]:
            logger.debug("before_request: %s", before_request.__name__)
            options = before_request(options)

        logger.debug(options)

        try:
            response = requests.request(**options)

        except Exception as e:
            # 异常处理
            if self._error_handler:
                return self._error_handler(e)
            else:
                raise e

        # 请求后响应处理
        for after_request in self._after_requests:
            logger.debug("after_request: %s", after_request.__name__)
            response = after_request(response)

        return response

    def route(self, url=None, method="GET", **options):

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                _url = url or func.__name__

                # 参数预处理
                result = func(*args, **kwargs)
                if result:
                    kwargs = result

                kwargs = {**options, 'method': method, 'url': _url, **kwargs}

                return self.request(**kwargs)

            return wrapper

        return decorator

    def get(self, url, **options):
        return self.route(url, method='GET', **options)

    def post(self, url, **options):
        return self.route(url, method='POST', **options)

    def delete(self, url, **options):
        return self.route(url, method='DELETE', **options)

    def options(self, url, **options):
        return self.route(url, method='OPTIONS', **options)

    def head(self, url, **options):
        return self.route(url, method='HEAD', **options)

    def put(self, url, **options):
        return self.route(url, method='PUT', **options)

    def patch(self, url, **options):
        return self.route(url, method='PATCH', **options)
