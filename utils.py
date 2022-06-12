# coding: utf-8
"""データに関係ないメソッドを提供します。"""
from typing import List
import re

import pprint

def check_input_data(data: str) -> bool:
    """文字列データを入力入力データに変換できるかチェックする

    チェックは正規表現でチェックするのみとします。
    """
    text = (
        r'^\d{9}\n{0,1}'
        r'\d{9}\n{0,1}'
        r'\d{9}\n{0,1}'
        r'\d{9}\n{0,1}'
        r'\d{9}\n{0,1}'
        r'\d{9}\n{0,1}'
        r'\d{9}\n{0,1}'
        r'\d{9}\n{0,1}'
        r'\d{9}\n{0,1}'
    )
    pattern = re.compile(text)
    matcher = pattern.match(data)
    if matcher:
        return True
    else:
        return False

def string2data(str_data:str) -> List[List[int]]:
    """string to data"""
    text = str_data
    text = text.replace('\n', '')

    data = []
    for index in range(9):
        data.append([int(v) for v in text[index * 9: (index+1) * 9]])
    return data

