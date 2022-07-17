# coding: utf-8
"""model module"""
from typing import List

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


class ValueModel:
    """セルの値を管理するためのモデルクラス"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def get_display_value(self) -> str:
        """画面表示用の文字列取得関数

        このプログラムでは0を空白として扱うので、0の場合は空白、そのほかの場合は
        文字列として返す処理です。
        """
        return str(self.value) if self.value > 0 else ''


class CandidatesModel:
    """セルの候補となる数字を管理するモデルクラス

    まだどの数字が入るかわからないセルの候補となる数字を管理するためのクラスです。
    """
    def __init__(self, value: int):
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

    def reset(self, value: bool) -> None:
        """指定した値を候補のリストをリセットします。"""
        for i in range(len(self.candidates)):
            self.candidates[i] = value

    def is_narrow_down(self) -> bool:
        """候補が一つに絞られているか確認するための処理"""
        if sum(self.candidates) == 1:
            return True
        return False

    def get_narrow_down(self) -> int:
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


class CellModel:
    """CellModel"""

    def __init__(self, value: int, status_model: StatusModel):
        self.value = value
        self.value_model = ValueModel(value)
        self.candidates = CandidatesModel(value)
        self.status_model = status_model

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
        self.value = value
        self.value_model.value = value
        if value > 0:
            self.candidates.reset(False)
        else:
            self.candidates.reset(True)

    def set_candidate(self, number: int, value: int) -> None:
        """候補の指定した数値のチェックを設定します。

        候補の数値は1~9で指定してください。
        """
        # TODO:いったん設定したものはすべて変更があったとみなす。
        self.status_model.changed()
        self.candidates.set_candidate(number, value)

    def is_narrow_down(self) -> bool:
        """候補が一つに絞られているかを取得します。"""
        return self.candidates.is_narrow_down()

    def get_narrow_down(self) -> int:
        """候補の中で一番小さい値を取得します。"""
        return self.candidates.get_narrow_down()


class BaseGroupModel:
    """BaseGroupModel"""
    def __init__(self, data: List[List[int]]):
        self.data = data

    def get_cell_models(self) -> List[List[int]]:
        """セルのデータを取得します。"""
        return self.data

    def compute_candidate(self) -> None:
        """グループに設定されているセルの値から候補を絞り込みます。"""
        for i, cells in enumerate(self.data):
            for j, cell in enumerate(cells):
                value = cell.get_value()
                if value > 0:
                    for i_2 in range(3):
                        for j_2 in range(3):
                            if i == i_2 and j == j_2:
                                pass
                            else:
                                check_cell = self.data[i_2][j_2]
                                if check_cell.get_value() > 0:
                                    pass
                                else:
                                    check_cell.set_candidate(value, False)
                else:
                    pass

    def select_from_candidate_in_group(self) -> None:
        """グループ内で候補として一つにしか設定されていない候補数字を値として設定する処理"""
        for i in range(9):
            count = 0
            handle = None
            is_exist = False
            for row in self.data:
                if is_exist:
                    break
                for cell in row:
                    if is_exist:
                        break
                    if cell.get_value() > 0:
                        if cell.get_value() == i + 1:
                            is_exist = True
                            break
                    else:
                        if cell.get_candidates()[i]:
                            count += 1
                            handle = cell
                        else:
                            pass
            if not is_exist and count == 1:
                handle.set_value(i + 1)


class SquareGroupModel(BaseGroupModel):
    """SquareModel"""
    # TODO: 正方形グループで特別に処理する処理は現状ありません。

class VerticalGroupModel(BaseGroupModel):
    """VerticalGroupModel"""
    # TODO: 縦列グループで特別に処理する処理は現状ありません。

class HorizontalGroupModel(BaseGroupModel):
    """HorizontalGroupModel"""
    # TODO: 横列グループで特別に処理する処理は現状ありません。

class CrossGroupModel(BaseGroupModel):
    """CrossGroupModel"""
    # TODO: クロスグループで特別に処理する処理は現状ありません。

class DataModel:
    """DataModel"""
    def __init__(self, data: List[List[int]]):
        # ステータス用のモデルクラス設定
        self.init_data = data

        self.status_model = StatusModel()
        self.cells = None

        # create groups
        self.square_groups = []
        self.vertical_groups = []
        self.horizontal_groups = []
        self.cross_groups = []

        self.initialize(data)

    def initialize(self, init_data: List[List[int]]):
        """データの初期設定"""
        self.init_data = init_data
        self.cells = [
            [CellModel(cell, self.status_model) for cell in row] for row in init_data]

        # create groups
        ## square groups
        self.square_groups = []
        for row in range(3):
            sgroups = []
            for col in range(3):
                data = [[self.cells[row * 3 + i][ col * 3 + j]
                        for j in range(3)]
                        for i in range(3)]
                sgroups.append(SquareGroupModel(data))
            self.square_groups.append(sgroups)
        ## vertical groups
        self.vertical_groups = []
        for group_index in range(3):
            vgroups = []
            for cell_index in range(3):
                data = [[self.cells[j * 3 + i][group_index * 3 + cell_index]
                        for i in range(3)]
                        for j in range(3)]
                vgroups.append(VerticalGroupModel(data))
            self.vertical_groups.append(vgroups)
        ## horizontal groups
        self.horizontal_groups = []
        for group_index in range(3):
            hgroups = []
            for cell_index in range(3):
                data = [[self.cells[group_index * 3 + cell_index][j * 3 + i]
                        for i in range(3)]
                        for j in range(3)]
                hgroups.append(HorizontalGroupModel(data))
            self.horizontal_groups.append(hgroups)
        ## cross groups
        self.cross_groups = []
        cgroups = []
        data = [[self.cells[i + 3 * j][i + 3 * j]
                for i in range(3)]
                for j in range(3)]
        cgroups.append(CrossGroupModel(data))
        data = [[self.cells[i + 3 * j][8 - (i + 3 * j)]
                for i in range(3)]
                for j in range(3)]
        cgroups.append(CrossGroupModel(data))
        self.cross_groups.append(cgroups)
        self.status_model.turn_start()

    def reset(self):
        """最初の状態(初期データ)に戻す"""
        self.initialize(self.init_data)

    def check_to_complete(self) -> bool:
        """数独を解き終わっているか確認する処理"""
        for row in self.cells:
            for cell in row:
                if cell.get_value() > 0:
                    pass
                else:
                    return False
        return True

    def get_init_data(self):
        """get init data"""
        return self.init_data

    def get_square_groups(self) -> List[List[SquareGroupModel]]:
        """get square_groups"""
        return self.square_groups

    def get_vertical_groups(self) -> List[List[VerticalGroupModel]]:
        """get vertical groups"""
        return self.vertical_groups

    def get_horizontal_groups(self) -> List[List[HorizontalGroupModel]]:
        """get horizontal groups"""
        return self.horizontal_groups

    def get_cross_groups(self) -> List[List[CrossGroupModel]]:
        """ get cross groups"""
        return self.cross_groups

    def select_from_candidate(self) -> None:
        """候補が一つに絞られているセルの値を設定する処理"""
        for cell_row in self.cells:
            for cell in cell_row:
                if cell.get_value() > 0:
                    pass
                else:
                    if cell.is_narrow_down():
                        index = cell.get_narrow_down()
                        cell.set_value(index)
                    else:
                        pass

    def select_from_candidate_in_square(self) -> None:
        """正方形グループ内で一つのセルにしか入らない値を設定する処理"""
        for square_row in self.square_groups:
            for square in square_row:
                square.select_from_candidate_in_group()

    def select_from_candidate_in_horizontal(self) -> None:
        """横列グループ内で一つのセルにしか入らない値を設定する処理"""
        for hgroup_row in self.horizontal_groups:
            for hgroup in hgroup_row:
                hgroup.select_from_candidate_in_group()

    def select_from_candidate_in_vertical(self) -> None:
        """縦列グループ内で一つのセルにしか入らない値を設定する処理"""
        for vgroup_row in self.vertical_groups:
            for vgroup in vgroup_row:
                vgroup.select_from_candidate_in_group()

    def select_from_candidate_in_cross(self) -> None:
        """クロスグループ内で一つのセルにしか入らない値を設定する処理"""
        for cgroup_row in self.cross_groups:
            for cgroup in cgroup_row:
                cgroup.select_from_candidate_in_group()

    def compute_square_candidate(self) -> None:
        """正方形内での候補値をチェックします。"""
        for sgroup_row in self.square_groups:
            for sgroup in sgroup_row:
                sgroup.compute_candidate()

    def compute_vertical_candidate(self) -> None:
        """縦列グループで候補値をチェックします。"""
        for vgroup_row in self.vertical_groups:
            for vgroup in vgroup_row:
                vgroup.compute_candidate()

    def compute_cross_candidate(self) -> None:
        """クロスグループで候補値をチェックします。"""
        for cgroup_row in self.cross_groups:
            for cgroup in cgroup_row:
                cgroup.compute_candidate()

    def compute_horizontal_candidate(self) -> None:
        """横列グループで候補値をチェックします。"""
        for hgroup_row in self.horizontal_groups:
            for hgroup in hgroup_row:
                hgroup.compute_candidate()

    def debug_print(self, only_one:bool=False) -> None:
        """デバッグとして値を確認するための出力処理"""
        index = 0
        for row in self.cells:
            for cell in row:
                index += 1
                print(f'{index:02}: value: {cell.get_value()} candidates: {cell.get_candidates()}')

                if only_one:
                    return

    def debug_print_square_groups(self) -> None:
        """デバッグとして正方形グループごとに値を確認するための出力処理"""
        row_index = 0
        for square_row in self.square_groups:
            row_index += 1
            col_index = 0
            for square in square_row:
                col_index += 1
                print(f'({row_index}, {col_index}) {square}')

    def is_changed(self) -> bool:
        """変更が発生したか確認する処理"""
        return self.status_model.is_changed()

    def start_turn(self) -> None:
        """処理開始前に呼ぶ処理"""
        return self.status_model.turn_start()
