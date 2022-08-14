# coding: utf-8
""""問題を解けるか確認"""
import os
import pathlib

import pytest

import models_v2 as models
import utils


def create_data():
    """create data"""
    base_path = pathlib.Path(__file__).parent.parent
    questions_path = base_path / 'questions'
    result = []
    for type_path in questions_path.glob('*'):
        type_code = type_path.name
        for path in type_path.glob('*'):
            result.append([type_code, path])

    return result

sample_data = create_data()

@pytest.mark.parametrize(('type_code', 'path'), sample_data,
        ids=[''.join([item[0], '-', item[1].name]) for item in sample_data])
def test_models(type_code, path):
    """問題が解けるか確認"""
    print()
    with open(path, 'r', encoding='utf-8') as file:
        str_data = file.read()
    result = False
    if type_code == 'normal':
        data = utils.string2data(str_data)
        model = models.DataModel(data)
        result = model.auto_complite_normal()
    elif type_code == 'cross':
        data = utils.string2data(str_data)
        model = models.DataModel(data)
        result = model.auto_complite_cross()
    elif type_code == 'jigsaw':
        str_data = str_data.replace('\n', '')
        str_data_data = str_data[:9*9]
        str_data_jigsaw = str_data[-9*9:]
        data = utils.string2data(str_data_data)
        jigsaw = utils.string2data(str_data_jigsaw)
        model = models.DataModel(data)
        model.set_pazzle_group(jigsaw)
        result = model.auto_complite_jigsaw()

    assert result
