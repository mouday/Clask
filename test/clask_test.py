# -*- coding: utf-8 -*-

import unittest
from .clask_demo import *


class ClaskTest(unittest.TestCase):

    def test_get(self):
        query = {"name": "Tom", "age": 23}
        print(get(query=query))

    def test_post1(self):
        data = {"name": "Jack", "age": 24}
        print(post1(json=data))

    def test_post2(self):
        data = {"name": "Jack", "age": 24}
        print(post2(json=data))

    def test_getStudent(self):
        print(getStudent(uid=1, name='Tom'))


if __name__ == '__main__':
    unittest.main()
