# coding: utf-8
"""モデルテスト"""
import pytest

import models


model_shape_datas = [
    ([[0 for _ in range(9)] for _ in range(9)],),
]

model_str_datas = [
    ([
        "129084305",
        "064503980",
        "503690000",
        "638457129",
        "945218673",
        "210000854",
        "470132590",
        "300075016",
        "001906702",
    ]),
]
model_datas = [
    ([[int(value) for value in row] for row in data],) for data in model_str_datas
]


@pytest.mark.parametrize(('model_data',), model_shape_datas)
def test_data_model(model_data):
    """DataModelを正常に生成できることを確認"""
    model = models.DataModel(model_data)
    assert model is not None

@pytest.mark.parametrize(('model_data',), model_datas)
def test_data_model_success(model_data):
    """モデルが正しく答えを求められるか確認"""
    model = models.DataModel(model_data)

    for _ in range(50):
        model.compute_square_candidate()
        model.compute_vertical_candidate()
        model.compute_horizontal_candidate()
        model.select_from_candidate()
        model.select_from_candidate_in_square()
        model.select_from_candidate_in_vertical()
        model.select_from_candidate_in_horizontal()
    assert model.check_to_complete() == True
