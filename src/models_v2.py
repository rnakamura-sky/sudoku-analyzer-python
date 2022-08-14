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


class CandidatesModel:
    """セルの候補となる数字を管理するモデルクラス

    まだどの数字が入るかわからないセルの候補となる数字を管理するためのクラスです。
    """
    def __init__(self, value:int):
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

    def __init__(self, value: int, status_model: StatusModel, row=None, col=None):
        # self.value = value
        self.value_model = ValueModel(value)
        self.candidates = CandidatesModel(value)
        self.status_model = status_model
        self.row = row
        self.col = col
        self.groups = dict()

    def reset(self):
        """リセットする"""
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
        self.candidates.set_candidate(number, value)

    def is_narrow_down(self) -> bool:
        """候補が一つに絞られているかを取得します。"""
        return self.candidates.is_narrow_down()

    def get_narrow_down(self) -> int:
        """候補の中で一番小さい値を取得します。"""
        return self.candidates.get_narrow_down()

    def get_row(self):
        """get row"""
        if self.row is None:
            raise ValueError()
        return self.row

    def get_col(self):
        """get col"""
        if self.col is None:
            raise ValueError()
        return self.col

    def set_group(self, group_name:str, group_id:id):
        """set group"""
        self.groups[group_name] = group_id

    def get_group(self, group_name):
        """get group"""
        group_id = self.groups.get(group_name)
        # if group_id is None:
        #     raise ValueError()
        return group_id


class BaseGroupModel:
    """BaseGroupModel"""
    group_name = 'base'

    def __init__(self, group_id:int, data:List[CellModel]):
        self.group_id = group_id
        self.data = data
        for cell in data:
            cell.set_group(self.group_name, group_id)

    def get_cell_models(self) -> List[List[int]]:
        """セルのデータを取得します。"""
        # cells = [[0 for _ in range(3)] for _ in range(3)]
        cells = [0 for _ in range(3) for _ in range(3)]
        for i in range(3):
            for j in range(3):
                # cells[i][j] = self.data[3 * i + j]
                cells[3 * i + j] = self.data[3 * i + j]
        return cells

    def get_group_id(self):
        """get group id"""
        return self.group_id

    def compute_candidate(self) -> None:
        """グループに設定されているセルの値から候補を絞り込みます。"""
        for i_1, cell in enumerate(self.data):
            value = cell.get_value()
            if value > 0:
                for i_2, check_cell in enumerate(self.data):
                    if i_1 == i_2:
                        pass
                    else:
                        check_value = check_cell.get_value()
                        if check_value > 0:
                            pass
                        else:
                            check_cell.set_candidate(value, False)
            else:
                pass

    def select_from_candidate_in_group(self) -> None:
        """グループ内で候補として一つにしか設定されていない候補数字を値として設定する処理"""
        # 1~9までの数字についてチェックを行う。
        for i in range(9):
            num = i + 1
            count = 0
            handle = None
            is_exist = False
            # cellすべてについてチェックを開始
            for cell in self.data:
                if cell.get_value() > 0:
                    # すでに数字が存在している場合は次の数字に進めてしまう。
                    if cell.get_value() == num:
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

    def check_pairs(self):
        """2つのcellで同じ2つの数字候補蚤の場合、他の場所に設定されることはないのでその処理"""
        cells = []
        pairs = []
        for cell in self.data:
            if cell.get_value() > 0:
                continue
            if sum(cell.get_candidates()) == 2:
                corr = False
                for stack in cells.copy():
                    if sum([a == b for a, b in zip(cell.get_candidates(), stack.get_candidates())]) == 9:
                        pair = [cell, stack]
                        pairs.append(pair)
                        corr = True
                        cells.remove(stack)
                        break
                if not corr:
                    cells.append(cell)
        for pair in pairs:
            cell1, _ = pair
            values = []
            for index, candidate in enumerate(cell1.get_candidates()):
                if candidate:
                    values.append(index + 1)
            for cell in self.data:
                if cell.get_value() > 0:
                    continue
                if cell in pair:
                    continue
                for value in values:
                    cell.set_candidate(value, False)

    def calc_only_id(self, group_name, number):
        """候補の値がgroup_nameで指定されたグループで一意に決まるか"""
        group_id = None
        for cell in self.data:
            if cell.get_value() == number:
                return None
            if cell.get_value() > 0:
                continue
            if cell.get_candidate(number):
                temp_group_id = cell.get_group(group_name)
                if group_id is None:
                    group_id = temp_group_id
                if group_id != temp_group_id:
                    return None
        return group_id

    def get_candidate_number_list(self, number):
        """get candidate number list"""
        result = []
        for cell in self.data:
            if cell.get_value() == number:
                return None
            elif cell.get_value() > 0:
                result.append(False)
            else:
                candidate = cell.get_candidate(number)
                result.append(candidate)
        return result

    def check_pairs_in_group(self):
        """check pairs in group"""
        temp_list = dict()
        for i in range(9):
            number = i + 1
            check_list = self.get_candidate_number_list(number)
            # print(check_list)
            if check_list is None:
                continue
            if sum(check_list) != 2:
                continue
            temp_list[number] = check_list
        # print(temp_list)
        pairs = dict()
        for key_1, value_1 in temp_list.items():
            for key_2, value_2 in temp_list.items():
                if key_1 >= key_2:
                    continue
                check_count = sum([v1 == v2 for v1, v2 in zip(value_1, value_2)])
                if check_count == 9:
                    pairs[(key_1, key_2)] = value_1
        # print(pairs)
        for numbers, values in pairs.items():
            for index, bool_value in enumerate(values):
                if bool_value:
                    for number in range(1, 10):
                        if number in numbers:
                            continue
                        self.data[index].set_candidate(number, False)


class SquareGroupModel(BaseGroupModel):
    """SquareModel"""
    group_name = 'square'

    def check_number_in_group(self, number):
        """check number in group"""
        rows = []
        cols = []
        for cell in self.data:
            if cell.get_value() == number:
                return None
            if cell.get_value() > 0:
                continue
            candidate = cell.get_candidate(number)
            # print(f'Candidate group_id:{self.group_id} number:{number} row:{cell.get_row()} col:{cell.get_col()} candidate:{candidate}')
            if candidate:
                row = cell.get_row()
                if row not in rows:
                    rows.append(row)
                col = cell.get_col()
                if col not in cols:
                    cols.append(col)
        row_index = None
        if len(rows) == 1:
            row_index = rows[0]
        col_index = None
        if len(cols) == 1:
            col_index = cols[0]
        result = {'row': row_index, 'col': col_index}

        return result

class VerticalGroupModel(BaseGroupModel):
    """VerticalGroupModel"""
    group_name = 'vertical'

class HorizontalGroupModel(BaseGroupModel):
    """HorizontalGroupModel"""
    group_name = 'horizontal'

class CrossGroupModel(BaseGroupModel):
    """CrossGroupModel"""
    group_name = 'cross'

class PazzleGroupModel(BaseGroupModel):
    """PazzleGroupModel"""
    group_name = 'pazzle'

    def check_number_in_group(self, number):
        """check number in group"""
        rows = []
        cols = []
        for cell in self.data:
            if cell.get_value() == number:
                return None
            if cell.get_value() > 0:
                continue
            candidate = cell.get_candidate(number)
            # print(f'Candidate group_id:{self.group_id} number:{number} row:{cell.get_row()} col:{cell.get_col()} candidate:{candidate}')
            if candidate:
                row = cell.get_row()
                if row not in rows:
                    rows.append(row)
                col = cell.get_col()
                if col not in cols:
                    cols.append(col)
        row_index = None
        if len(rows) == 1:
            row_index = rows[0]
        col_index = None
        if len(cols) == 1:
            col_index = cols[0]
        result = {'row': row_index, 'col': col_index}

        return result


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
        self.pazzle_groups = []

        self.initialize(data)

    def initialize(self, init_data: List[List[int]]):
        """データの初期設定"""
        self.init_data = init_data
        self.cells = [
            [CellModel(cell, self.status_model, col=c_i, row=r_i)
                for c_i, cell in enumerate(row)]
                    for r_i, row in enumerate(init_data)]

        # create groups
        ## square groups
        self.square_groups = []
        for row in range(3):
            for col in range(3):
                data = [self.cells[3 * row + i][3 * col + j] for i in range(3) for j in range(3)]
                group_id = 3 * row + col
                self.square_groups.append(SquareGroupModel(group_id, data))
        ## vertical groups
        self.vertical_groups = []
        for index in range(9):
            data = [self.cells[i * 3 + j][index] for i in range(3) for j in range(3)]
            group_id = index
            self.vertical_groups.append(VerticalGroupModel(group_id, data))
        ## horizontal groups
        self.horizontal_groups = []
        for index in range(9):
            data = [self.cells[index][i * 3 + j] for i in range(3) for j in range(3)]
            group_id = index
            self.horizontal_groups.append(HorizontalGroupModel(group_id, data))
        ## cross groups
        self.cross_groups = []
        data = [self.cells[i + 3 * j][i + 3 * j] for i in range(3) for j in range(3)]
        self.cross_groups.append(CrossGroupModel(0, data))
        data = [self.cells[i + 3 * j][8 - (i + 3 * j)] for i in range(3) for j in range(3)]
        self.cross_groups.append(CrossGroupModel(1, data))
        self.status_model.turn_start()

    def update(self, init_data: List[List[int]]):
        """更新"""
        self.init_data = init_data
        for row_i, row_values in enumerate(init_data):
            for col_i, cell_value in enumerate(row_values):
                self.cells[row_i][col_i].set_value(cell_value)

        self.status_model.turn_start()

    def reset(self):
        """最初の状態(初期データ)に戻す"""
        self.update(self.init_data)

    def set_pazzle_group(self, group):
        """ジグソーグループを設定"""
        self.pazzle_groups = []
        datas = [[] for _ in range(9)]
        for row, values  in enumerate(group):
            for col, value in enumerate(values):
                datas[value-1].append(self.cells[row][col])
        for group_id, data in enumerate(datas):
            self.pazzle_groups.append(PazzleGroupModel(group_id, data))


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

    def get_square_groups(self) -> List[SquareGroupModel]:
        """get square_groups"""
        return self.square_groups

    def get_vertical_groups(self) -> List[VerticalGroupModel]:
        """get vertical groups"""
        return self.vertical_groups

    def get_horizontal_groups(self) -> List[HorizontalGroupModel]:
        """get horizontal groups"""
        return self.horizontal_groups

    def get_cross_groups(self) -> List[CrossGroupModel]:
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
        for square in self.square_groups:
            square.select_from_candidate_in_group()

    def select_from_candidate_in_horizontal(self) -> None:
        """横列グループ内で一つのセルにしか入らない値を設定する処理"""
        for hgroup in self.horizontal_groups:
            hgroup.select_from_candidate_in_group()

    def select_from_candidate_in_vertical(self) -> None:
        """縦列グループ内で一つのセルにしか入らない値を設定する処理"""
        for vgroup in self.vertical_groups:
            vgroup.select_from_candidate_in_group()

    def select_from_candidate_in_cross(self) -> None:
        """クロスグループ内で一つのセルにしか入らない値を設定する処理"""
        for cgroup in self.cross_groups:
            cgroup.select_from_candidate_in_group()

    def select_from_candidate_in_pazzle(self) -> None:
        """ジグソーグループ内で一つのセルにしか入らない値を設定する処理"""
        for pgroup in self.pazzle_groups:
            pgroup.select_from_candidate_in_group()

    def select_other_squares(self) -> None:
        """select others"""
        # グループの関連
        # グループ内で指定された数字の行、列が決まる場合は、他のグループから除く
        for square in self.square_groups:
            for number in range(1, 10):
                stats = square.check_number_in_group(number)
                if stats is None:
                    continue
                group_id = square.get_group_id()
                row = stats['row']
                col = stats['col']
                if row is not None:
                    # print(f'test group:{group_id}, number:{number}, row:{row}')
                    for row_cells in self.cells:
                        for cell in row_cells:
                            if cell.get_row() == row and cell.get_group('square') != group_id:
                                cell.set_candidate(number, False)
                if col is not None:
                    if group_id == 6:
                        print(f'test group:{group_id}, number:{number}, col:{col}')
                    for row_cells in self.cells:
                        for cell in row_cells:
                            if cell.get_col() == col and cell.get_group('square') != group_id:
                                cell.set_candidate(number, False)

    def select_other_pazzles(self) -> None:
        """select others"""
        # グループの関連
        # グループ内で指定された数字の行、列が決まる場合は、他のグループから除く
        for pazzle in self.pazzle_groups:
            for number in range(1, 10):
                stats = pazzle.check_number_in_group(number)
                if stats is None:
                    continue
                group_id = pazzle.get_group_id()
                row = stats['row']
                col = stats['col']
                if row is not None:
                    # print(f'test group:{group_id}, number:{number}, row:{row}')
                    for row_cells in self.cells:
                        for cell in row_cells:
                            if cell.get_row() == row and cell.get_group('pazzle') != group_id:
                                cell.set_candidate(number, False)
                if col is not None:
                    if group_id == 6:
                        print(f'test group:{group_id}, number:{number}, col:{col}')
                    for row_cells in self.cells:
                        for cell in row_cells:
                            if cell.get_col() == col and cell.get_group('pazzle') != group_id:
                                cell.set_candidate(number, False)


    def compute_square_candidate(self) -> None:
        """正方形内での候補値をチェックします。"""
        for sgroup in self.square_groups:
            sgroup.compute_candidate()

    def compute_vertical_candidate(self) -> None:
        """縦列グループで候補値をチェックします。"""
        for vgroup in self.vertical_groups:
            vgroup.compute_candidate()

    def compute_cross_candidate(self) -> None:
        """クロスグループで候補値をチェックします。"""
        for cgroup in self.cross_groups:
            cgroup.compute_candidate()

    def compute_horizontal_candidate(self) -> None:
        """横列グループで候補値をチェックします。"""
        for hgroup in self.horizontal_groups:
            hgroup.compute_candidate()

    def compute_pazzle_candidate(self) -> None:
        """ジグソーグループで候補値をチェックします。"""
        for pgroup in self.pazzle_groups:
            pgroup.compute_candidate()

    def check_pairs_square(self) -> None:
        """check pairs"""
        for vgroup in self.vertical_groups:
            vgroup.check_pairs()
        for hgroup in self.horizontal_groups:
            hgroup.check_pairs()
        for sgroup in self.square_groups:
            sgroup.check_pairs()

    def check_pairs_cross(self) -> None:
        """check pairs"""
        for vgroup in self.vertical_groups:
            vgroup.check_pairs()
        for hgroup in self.horizontal_groups:
            hgroup.check_pairs()
        for sgroup in self.square_groups:
            sgroup.check_pairs()
        for cgroup in self.cross_groups:
            cgroup.check_pairs()

    def check_pairs_pazzle(self) -> None:
        """check pairs"""
        for vgroup in self.vertical_groups:
            vgroup.check_pairs()
        for hgroup in self.horizontal_groups:
            hgroup.check_pairs()
        for pgroup in self.pazzle_groups:
            pgroup.check_pairs()

    def compute_others_square(self):
        """compute others square"""
        from_group_name = 'vertical'
        to_group_name = 'square'
        for v_index, vgroup in enumerate(self.vertical_groups):
            for number in range(1, 10):
                only_id = vgroup.calc_only_id(to_group_name, number)
                if only_id is not None:
                    for rows in self.cells:
                        for cell in rows:
                            if cell.get_value() > 0:
                                continue
                            group_id = cell.get_group(to_group_name)
                            if group_id == only_id:
                                v_group_id = cell.get_group(from_group_name)
                                if v_index != v_group_id:
                                    cell.set_candidate(number, False)
        from_group_name = 'horizontal'
        to_group_name = 'square'
        for h_index, hgroup in enumerate(self.horizontal_groups):
            for number in range(1, 10):
                only_id = hgroup.calc_only_id(to_group_name, number)
                if only_id is not None:
                    for rows in self.cells:
                        for cell in rows:
                            if cell.get_value() > 0:
                                continue
                            group_id = cell.get_group(to_group_name)
                            if group_id == only_id:
                                h_group_id = cell.get_group(from_group_name)
                                if h_index != h_group_id:
                                    cell.set_candidate(number, False)

    def compute_others_cross(self):
        """compute others square"""
        self.compute_others_square()
        from_group_name = 'cross'
        to_group_name = 'square'
        for c_index, cgroup in enumerate(self.cross_groups):
            for number in range(1, 10):
                only_id = cgroup.calc_only_id(to_group_name, number)
                if only_id is not None:
                    for rows in self.cells:
                        for cell in rows:
                            if cell.get_value() > 0:
                                continue
                            group_id = cell.get_group(to_group_name)
                            if group_id == only_id:
                                c_group_id = cell.get_group(from_group_name)
                                if c_group_id is None:
                                    continue
                                if c_index != c_group_id:
                                    cell.set_candidate(number, False)

    def compute_others_pazzle(self):
        """compute others square"""
        from_group_name = 'vertical'
        to_group_name = 'pazzle'
        for v_index, vgroup in enumerate(self.vertical_groups):
            for number in range(1, 10):
                only_id = vgroup.calc_only_id(to_group_name, number)
                if only_id is not None:
                    for rows in self.cells:
                        for cell in rows:
                            if cell.get_value() > 0:
                                continue
                            group_id = cell.get_group(to_group_name)
                            if group_id == only_id:
                                v_group_id = cell.get_group(from_group_name)
                                if v_index != v_group_id:
                                    cell.set_candidate(number, False)
        from_group_name = 'horizontal'
        to_group_name = 'pazzle'
        for h_index, hgroup in enumerate(self.horizontal_groups):
            for number in range(1, 10):
                only_id = hgroup.calc_only_id(to_group_name, number)
                if only_id is not None:
                    for rows in self.cells:
                        for cell in rows:
                            if cell.get_value() > 0:
                                continue
                            group_id = cell.get_group(to_group_name)
                            if group_id == only_id:
                                h_group_id = cell.get_group(from_group_name)
                                if h_index != h_group_id:
                                    cell.set_candidate(number, False)

    def check_pairs_in_group_normal(self):
        """check pairs in group normal"""
        for hgroup in self.horizontal_groups:
            hgroup.check_pairs_in_group()
        for vgroup in self.vertical_groups:
            vgroup.check_pairs_in_group()
        for sgroup in self.square_groups:
            sgroup.check_pairs_in_group()

    def check_pairs_in_group_cross(self):
        """check pairs in group normal"""
        for hgroup in self.horizontal_groups:
            hgroup.check_pairs_in_group()
        for vgroup in self.vertical_groups:
            vgroup.check_pairs_in_group()
        for sgroup in self.square_groups:
            sgroup.check_pairs_in_group()
        for cgroup in self.cross_groups:
            cgroup.check_pairs_in_group()

    def check_pairs_in_group_jigsaw(self):
        """check pairs in group normal"""
        for hgroup in self.horizontal_groups:
            hgroup.check_pairs_in_group()
        for vgroup in self.vertical_groups:
            vgroup.check_pairs_in_group()
        for pgroup in self.pazzle_groups:
            pgroup.check_pairs_in_group()

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
        for index, square in enumerate(self.square_groups):
            row_index = index % 3 + 1
            col_index = index // 3 + 1
            print(f'({row_index}, {col_index}) {square}')

    def is_changed(self) -> bool:
        """変更が発生したか確認する処理"""
        return self.status_model.is_changed()

    def start_turn(self) -> None:
        """処理開始前に呼ぶ処理"""
        return self.status_model.turn_start()

    def auto_complite_normal(self, max_turn=50) -> bool:
        """自動計算"""
        result = False
        for _ in range(max_turn):
            self.compute_square_candidate()
            self.compute_horizontal_candidate()
            self.compute_vertical_candidate()

            self.select_from_candidate_in_square()
            self.select_from_candidate_in_horizontal()
            self.select_from_candidate_in_vertical()

            self.select_other_squares()

            self.check_pairs_square()
            self.compute_others_square()
            self.check_pairs_in_group_normal()

            self.select_from_candidate()
            result = self.check_to_complete()
            if result:
                break
        return result

    def auto_complite_cross(self, max_turn=50) -> bool:
        """自動計算"""
        result = False
        for _ in range(max_turn):
            self.compute_square_candidate()
            self.compute_horizontal_candidate()
            self.compute_vertical_candidate()
            self.compute_cross_candidate()

            self.select_from_candidate_in_square()
            self.select_from_candidate_in_horizontal()
            self.select_from_candidate_in_vertical()
            self.select_from_candidate_in_cross()

            self.select_other_squares()

            self.check_pairs_cross()
            self.compute_others_cross()
            self.check_pairs_in_group_cross()

            self.select_from_candidate()
            result = self.check_to_complete()
            if result:
                break
        return result

    def auto_complite_jigsaw(self, max_turn=50) -> bool:
        """自動計算"""
        result = False
        for _ in range(max_turn):
            self.compute_pazzle_candidate()
            self.compute_horizontal_candidate()
            self.compute_vertical_candidate()

            self.select_from_candidate_in_pazzle()
            self.select_from_candidate_in_horizontal()
            self.select_from_candidate_in_vertical()

            self.select_other_pazzles()

            self.check_pairs_pazzle()
            self.compute_others_pazzle()
            self.check_pairs_in_group_jigsaw()

            self.select_from_candidate()
            result = self.check_to_complete()
            if result:
                break
        return result
