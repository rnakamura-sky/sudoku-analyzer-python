# coding: utf-8
"""モデルテスト"""
import pytest

import models


model_datas = [
    ([[0 for _ in range(9)] for _ in range(9)],),
]


@pytest.mark.parametrize(('model_data',), model_datas)
def test_data_model(model_data):
    """DataModelを正常に生成できることを確認"""
    model = models.DataModel(model_data)
    assert model is not None
