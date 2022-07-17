# coding: utf-8
"""モデルテスト"""
import pytest

import models


@pytest.fixture
def model_data():
    return [[0 for _ in range(9)] for _ in range(9)]



def test_data_model(model_data):
    """DataModelを正常に生成できることを確認"""


    model = models.DataModel(model_data)

    assert model is not None
