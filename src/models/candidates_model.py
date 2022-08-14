# coding: utf-8
"""candidates model"""
from typing import List, Optional


class CandidatesModel:
    """セルの候補となる数字を管理するモデルクラス

    まだどの数字が入るかわからないセルの候補となる数字を管理するためのクラスです。
    """
    def __init__(self, value:int) -> None:
        """__init__

        valueはセルの値となります。0~9が入りますが、0の場合は、数字が未設定であるという
        仕様のため、初期値としてすべて候補であるという状態にします。
        """
        if value > 0:
            self.candidates = [False for _ in range(9)]
        else:
            self.candidates = [True for _ in range(9)]

    def get_values(self) -> List[bool]:
        """候補となる値の配列を取得します。

        候補となる数字は1~9で、配列のインデックスは0~8で管理されます。
        読み替えが必要なため、注意してください。
        """
        return self.candidates

    def set_candidate(self, number: int, value: bool) -> None:
        """指定した数値が候補となるかならないかを設定します。"""
        self.candidates[number - 1] = value

    def get_candidate(self, number:int) -> bool:
        """get candidate"""
        return self.candidates[number - 1]

    def reset(self, value: bool) -> None:
        """指定した値を候補のリストをリセットします。"""
        for i in range(len(self.candidates)):
            self.candidates[i] = value

    def is_narrow_down(self) -> bool:
        """候補が一つに絞られているか確認するための処理"""
        if sum(self.candidates) == 1:
            return True
        return False

    def get_narrow_down(self) -> Optional[int]:
        """候補となる値を取得するための処理

        候補の中で一番小さい値を返す(一つに絞られている場合はその一つが返る)
        数値は1~9の値で返します。
        """
        index = 0
        for candidate in self.candidates:
            index += 1
            if candidate:
                return index
        return None
