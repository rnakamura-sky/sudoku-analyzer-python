# coding: utf-8
""""問題を解けるか確認"""
import pathlib

import pytest

import models
import utils


def create_data():
    """create data"""
    base_path = pathlib.Path(__file__).parent.parent
    questions_path = base_path / 'questions'
    result = []
    for type_path in questions_path.glob('*'):
        type_code = type_path.name
        for path in type_path.glob('*'):
            flag = True
            if str(path.name).endswith('_x.txt'):
                flag = False
            result.append([type_code, path, flag])

    return result

def check_group_data(group):
    """check group data"""
    data = [cell.get_value() for cell in group.data]
    set_data = set(data)
    if len(set_data) == 9:
        return True
    else:
        return False

sample_data = create_data()

@pytest.mark.parametrize(('type_code', 'path', 'flag'), sample_data,
        ids=[''.join([item[0], '-', item[1].name]) for item in sample_data])
def test_models(type_code, path, flag):
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

    assert result == flag
    if flag:
        for vgroup in model.get_vertical_groups():
            assert check_group_data(vgroup)
        for hgroup in model.get_horizontal_groups():
            assert check_group_data(hgroup)
        if type_code == 'normal':
            for sgroup in model.get_square_groups():
                assert check_group_data(sgroup)
        elif type_code == 'cross':
            for sgroup in model.get_square_groups():
                assert check_group_data(sgroup)
            for cgroup in model.get_cross_groups():
                assert check_group_data(cgroup)
        elif type_code == 'jigsaw':
            for jgroup in model.get_jigsaw_groups():
                assert check_group_data(jgroup)
