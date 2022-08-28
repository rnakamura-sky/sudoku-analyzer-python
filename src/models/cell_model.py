# coding: utf-8
"""cell model"""
from typing import List, Optional
import logging

import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CellModel:
    """CellModel"""

    def __init__(self, value: int, status_model: models.StatusModel, row=None, col=None) -> None:
        self.value_model = models.ValueModel(value)
        self.candidates = models.CandidatesModel(value)
        self.status_model = status_model
        self.row = row
        self.col = col
        self.groups = dict()

    def reset(self) -> None:
        """リセットする

        値は設定されず、すべて候補となっている状態にする。
        """
        self.value_model.reset()
        self.candidates.reset(True)

    def get_value(self) -> int:
        """セルの値を取得します。

        空白の場合は0が返ります。
        """
        return self.value_model.value

    def get_display_value(self) -> str:
        """セルの値を文字列で返します。

        0(空白)の場合は長さ0の文字列が返ります。
        そのほかの時は数値を文字列として返します。
        """
        return self.value_model.get_display_value()

    def get_candidates(self) -> List[bool]:
        """候補となる数値の候補チェックリストを取得します。

        配列は0~8でアクセスします。1~9の値についてのリストのため、読み替えが発生するので注意してください。
        """
        return self.candidates.get_values()

    def set_value(self, value: int) -> None:
        """セルの値を設定する処理です。"""
        # TODO:いったん設定したものはすべて変更があったとみなす。
        self.status_model.changed()
        self.value_model.value = value
        if value > 0:
            logger.info('Set value row:%s, col:%s, value:%s', self.row+1, self.col+1, value)
            self.candidates.reset(False)
        else:
            self.candidates.reset(True)

    def get_candidate(self, number:int) -> bool:
        """get candidate"""
        return self.candidates.get_candidate(number)

    def set_candidate(self, number: int, value: bool) -> None:
        """候補の指定した数値のチェックを設定します。

        候補の数値は1~9で指定してください。
        """
        # TODO:いったん設定したものはすべて変更があったとみなす。
        self.status_model.changed()
        if not value:
            if self.candidates.get_candidate(number):
                logger.info('Set Candidate Off row:%s, col:%s, number:%s', self.row+1, self.col+1, number)
        self.candidates.set_candidate(number, value)

    def is_narrow_down(self) -> bool:
        """候補が一つに絞られているかを取得します。"""
        return self.candidates.is_narrow_down()

    def get_narrow_down(self) -> int:
        """候補の中で一番小さい値を取得します。"""
        return self.candidates.get_narrow_down()

    def get_row(self) -> int:
        """セルの行を取得"""
        if self.row is None:
            raise ValueError()
        return self.row

    def get_col(self) -> int:
        """セルの列を取得"""
        if self.col is None:
            raise ValueError()
        return self.col

    def set_group(self, group_name:str, group_id:int) -> None:
        """指定されたグループのidを設定"""
        self.groups[group_name] = group_id

    def get_group(self, group_name) -> Optional[int]:
        """指定されたグループの所属idを取得

        設定されていない場合はNoneが返る
        """
        group_id = self.groups.get(group_name)
        return group_id
