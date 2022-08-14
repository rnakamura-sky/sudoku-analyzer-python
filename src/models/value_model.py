# coding: utf-8
"""value model"""

class ValueModel:
    """セルの値を管理するためのモデルクラス

    保持する値はNoneを持たない想定です。
    """

    def __init__(self, value:int=0) -> None:
        if value is None:
            raise ValueError('Noneを設定することはできません。')
        self.value = value

    def reset(self) -> None:
        """数字を初期化します

        初期化の値は0とします。
        """
        self.value = 0

    def get_value(self) -> int:
        """値を取得"""
        return self.value

    def set_value(self, value:int) -> None:
        """値を設定"""
        if value is None:
            raise ValueError('Noneを設定することはできません。')
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def get_display_value(self) -> str:
        """画面表示用の文字列取得関数

        このプログラムでは0を空白として扱うので、0の場合は空白、そのほかの場合は
        文字列として返す処理です。
        """
        return str(self.value) if self.value > 0 else ''
