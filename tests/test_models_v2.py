# coding: utf-8
"""モデルテスト"""
import pytest
# from models import CellModel

import models_v2 as models


model_shape_datas = [
    ([[0 for _ in range(9)] for _ in range(9)],),
]

model_str_datas = [
    (
        'normal',
        [
            "129084305",
            "064503980",
            "503690000",
            "638457129",
            "945218673",
            "210000854",
            "470132590",
            "300075016",
            "001906702",
        ],
        None
    ),
    (
        'cross',
        [
            "040001000",
            "000500900",
            "290600001",
            "901000600",
            "700300008",
            "005200009",
            "689027000",
            "050000090",
            "407905862",
        ],
        None
    ),
    (
        'pazzle',
        [
            "004052160",
            "007030814",
            "350079482",
            "403615009",
            "001090006",
            "009040501",
            "610503047",
            "038461795",
            "095720638",
        ],
        [
            "112222223",
            "412225533",
            "411655533",
            "411655533",
            "411666533",
            "444667788",
            "944667788",
            "999977788",
            "999977888",
        ],
    ),
]
model_datas = [
    (
        t,
        [[int(value) for value in row] for row in data],
        [[int(value) for value in row] for row in pazzle] if pazzle is not None else None
    ) for t, data, pazzle in model_str_datas
]


@pytest.mark.parametrize(('model_data',), model_shape_datas)
def test_data_model(model_data):
    """DataModelを正常に生成できることを確認"""
    model = models.DataModel(model_data)
    assert model is not None


@pytest.mark.parametrize(('sudoku_type', 'model_data', 'group'), model_datas)
def test_group_model_shape(sudoku_type, model_data, group):
    """グループのサイズが想定通りか確認"""
    model = models.DataModel(model_data)
    square_group_models = model.get_square_groups()
    assert len(square_group_models) == 9
    square_group_model = square_group_models[0]
    assert type(square_group_model) == models.SquareGroupModel

@pytest.mark.parametrize(('sudoku_type', 'model_data', 'group'), model_datas)
def test_data_model_success(sudoku_type, model_data, group):
    """モデルが正しく答えを求められるか確認"""
    model = models.DataModel(model_data)

    if sudoku_type == 'pazzle':
        model.set_pazzle_group(group)

    for _ in range(50):
        if sudoku_type == 'pazzle':
            model.compute_pazzle_candidate()
        else:
            model.compute_square_candidate()
        model.compute_vertical_candidate()
        model.compute_horizontal_candidate()
        if sudoku_type == 'cross':
            model.compute_cross_candidate()
        model.select_from_candidate()
        if sudoku_type == 'pazzle':
            model.select_from_candidate_in_pazzle()
        else:
            model.select_from_candidate_in_square()
        model.select_from_candidate_in_vertical()
        model.select_from_candidate_in_horizontal()
        if sudoku_type == 'cross':
            model.select_from_candidate_in_cross()
    assert model.check_to_complete() == True

@pytest.mark.parametrize(('sudoku_type', 'model_data', 'group'), model_datas)
def test_data_model_reset_success(sudoku_type, model_data, group):
    """モデルを一度リセットしても正しく答えを求められるか確認"""
    model = models.DataModel(model_data)
    model.update(model_data)

    if sudoku_type == 'pazzle':
        model.set_pazzle_group(group)

    for _ in range(50):
        if sudoku_type == 'pazzle':
            model.compute_pazzle_candidate()
        else:
            model.compute_square_candidate()
        model.compute_vertical_candidate()
        model.compute_horizontal_candidate()
        if sudoku_type == 'cross':
            model.compute_cross_candidate()
        model.select_from_candidate()
        if sudoku_type == 'pazzle':
            model.select_from_candidate_in_pazzle()
        else:
            model.select_from_candidate_in_square()
        model.select_from_candidate_in_vertical()
        model.select_from_candidate_in_horizontal()
        if sudoku_type == 'cross':
            model.select_from_candidate_in_cross()
    assert model.check_to_complete()


cell_datas = [
    (0, [True for _ in range(9)]),
    (1, [False for _ in range(9)]),
    (2, [False for _ in range(9)]),
    (3, [False for _ in range(9)]),
    (4, [False for _ in range(9)]),
    (5, [False for _ in range(9)]),
    (6, [False for _ in range(9)]),
    (7, [False for _ in range(9)]),
    (8, [False for _ in range(9)]),
    (9, [False for _ in range(9)]),
]

@pytest.mark.parametrize(('value', 'candidates'), cell_datas)
def test_cell_model(value, candidates):
    """CellModelがちゃんと生成できること"""
    status_model = models.StatusModel()
    cell_model = models.CellModel(value, status_model)

    assert cell_model.get_value() == value
    for i, candidate in enumerate(cell_model.get_candidates()):
        assert candidate == candidates[i]

    # リセット時の動き
    cell_model.reset()
    assert cell_model.get_value() == 0
    for candidate in cell_model.get_candidates():
        assert candidate

cell_candidates = [
    ([True, False, False, False, False, False, False, False, False], 1),
    ([False, True, False, False, False, False, False, False, False], 2),
    ([False, False, True, False, False, False, False, False, False], 3),
    ([False, False, False, True, False, False, False, False, False], 4),
    ([False, False, False, False, True, False, False, False, False], 5),
    ([False, False, False, False, False, True, False, False, False], 6),
    ([False, False, False, False, False, False, True, False, False], 7),
    ([False, False, False, False, False, False, False, True, False], 8),
    ([False, False, False, False, False, False, False, False, True], 9),
]

@pytest.mark.parametrize(('candidates', 'value'), cell_candidates)
def test_cell_model_candidate(candidates, value):
    """セルが一つに絞られているときの動き"""
    status_model = models.StatusModel()
    cell_model = models.CellModel(0, status_model)

    for i, candidate in enumerate(candidates):
        number = i + 1
        cell_model.set_candidate(number, candidate)

    assert cell_model.is_narrow_down()
    assert cell_model.get_narrow_down() == value

    assert cell_model.get_value() == 0
    cell_model.set_value(value)
    assert cell_model.get_value() == value

def create_cell(value, status_model, candidates=None):
    """create cell"""
    cell = models.CellModel(value, status_model)
    if value > 0:
        return cell
    for num in range(1, 10):
        if num in candidates:
            cell.set_candidate(num, True)
        else:
            cell.set_candidate(num, False)
    return cell

def test_group_pairs_1():
    """test group pairs"""
    data = []
    status_model = models.StatusModel()
    data.append(create_cell(0, status_model, [1, 3, 4, 5]))
    data.append(create_cell(9, status_model))
    data.append(create_cell(8, status_model))
    data.append(create_cell(0, status_model, [4, 5]))
    data.append(create_cell(0, status_model, [1, 3, 4, 5]))
    data.append(create_cell(0, status_model, [4, 5]))
    data.append(create_cell(6, status_model))
    data.append(create_cell(7, status_model))
    data.append(create_cell(2, status_model))

    group = models.BaseGroupModel(group_id=1, data=data)
    group.check_pairs()

    assert data[0].get_candidates() == [True, False, True, False, False, False, False, False, False]
    assert data[1].get_value() == 9
    assert data[2].get_value() == 8
    assert data[3].get_candidates() == [False, False, False, True, True, False, False, False, False]
    assert data[4].get_candidates() == [True, False, True, False, False, False, False, False, False]
    assert data[5].get_candidates() == [False, False, False, True, True, False, False, False, False]
    assert data[6].get_value() == 6
    assert data[7].get_value() == 7
    assert data[8].get_value() == 2

def test_group_pairs_2():
    """test group pairs"""
    data = []
    status_model = models.StatusModel()
    data.append(create_cell(0, status_model, [4, 5]))
    data.append(create_cell(0, status_model, [1, 3]))
    data.append(create_cell(0, status_model, [4, 5]))
    data.append(create_cell(0, status_model, [1, 2, 4, 5, 8, 9]))
    data.append(create_cell(0, status_model, [1, 2, 4, 5, 8]))
    data.append(create_cell(0, status_model, [2, 3, 4, 5, 8]))
    data.append(create_cell(7, status_model))
    data.append(create_cell(6, status_model))
    data.append(create_cell(0, status_model, [1, 5, 8, 9]))

    group = models.BaseGroupModel(group_id=1, data=data)
    group.check_pairs()

    assert data[0].get_candidates() == [False, False, False, True, True, False, False, False, False]
    assert data[1].get_candidates() == [True, False, True, False, False, False, False, False, False]
    assert data[2].get_candidates() == [False, False, False, True, True, False, False, False, False]
    assert data[3].get_candidates() == [True, True, False, False, False, False, False, True, True]
    assert data[4].get_candidates() == [True, True, False, False, False, False, False, True, False]
    assert data[5].get_candidates() == [False, True, True, False, False, False, False, True, False]
    assert data[6].get_value() == 7
    assert data[7].get_value() == 6
    assert data[8].get_candidates() == [True, False, False, False, False, False, False, True, True]