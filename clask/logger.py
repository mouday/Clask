# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, unicode_literals

import logging

logger = logging.getLogger('Clask')

logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(asctime)s - %(funcName)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
