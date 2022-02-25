#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

SPACE_TOKEN = ['']
NUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ALPHA_UPPER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']

SIMPLE_CATEGORY_MODEL = dict(
    ALPHANUMERIC_UPPER=NUMBER + ALPHA_UPPER,
)


def encode_maps(source):
    return {category: i for i, category in enumerate(source, 0)}
