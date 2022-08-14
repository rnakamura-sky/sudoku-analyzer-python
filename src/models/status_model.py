# coding: utf-8
"""status model"""

class StatusModel:
    """StatusModel

    行った作業で変更が発生したかどうかを管理します。
    変更を行った関数で戻り値に変更が発生したかどうか返す方法もありますが、
    今後どこをどう変化させたいというのを管理しようと思ったときに管理しやすいよう
    このクラスで管理します。
    TODO: シングルトンにしてもよいかなと思ったんですが、まずは引数で渡して実装しようと思います。
    """

    def __init__(self):
        """__init__"""
        self.__changed = False

    def turn_start(self) -> None:
        """処理開始の初期化を行う処理

        この処理を行った後に変更がくわえられたかを管理するため、
        その初期化処理を行います。
        この処理を行わなくても処理は正しく動きますが、変更の有無を
        管理する場合はこの処理を開始前に呼んでください。
        """
        self.__changed = False

    def changed(self) -> None:
        """変更が発生したことを記録する処理

        start_turnを実行後にこの処理行うと、is_changedで変更があったことを確認することができます。
        再びstart_turnを行うと変更があったことがリセットされます。
        """
        self.__changed = True

    def is_changed(self) -> bool:
        """変更があったことを確認するための処理"""
        return self.__changed
