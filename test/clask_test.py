# -*- coding: utf-8 -*-

import unittest
from .clask_demo import *


class ClaskTest(unittest.TestCase):

    def test_get(self):
        args = {"name": "Tom", "age": 23}
        res = get(args=args)
        print(res)

    def test_post1(self):
        data = {"name": "Jack", "age": 24}
        print(post1(json=data))

    def test_post2(self):
        data = {"name": "Jack", "age": 24}
        print(post2(json=data))


if __name__ == '__main__':
    unittest.main()
