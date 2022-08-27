# coding: utf-8
"""data model"""
from typing import List

import models


class DataModel:
    """DataModel"""
    def __init__(self, data: List[List[int]]) -> None:
        # ステータス用のモデルクラス設定
        self.init_data = data
        self.jigsaw_data = None

        self.status_model = models.StatusModel()
        self.cells = None

        # create groups
        self.square_groups = []
        self.vertical_groups = []
        self.horizontal_groups = []
        self.cross_groups = []
        self.pazzle_groups = []

        self.initialize(data)

    def initialize(self, init_data: List[List[int]]) -> None:
        """データの初期設定"""
        self.init_data = init_data
        self.cells = [
            [models.CellModel(cell, self.status_model, col=c_i, row=r_i)
                for c_i, cell in enumerate(row)]
                    for r_i, row in enumerate(init_data)]

        # create groups
        ## square groups
        self.square_groups = []
        for row in range(3):
            for col in range(3):
                data = [self.cells[3 * row + i][3 * col + j] for i in range(3) for j in range(3)]
                group_id = 3 * row + col
                self.square_groups.append(models.SquareGroupModel(group_id, data))
        ## vertical groups
        self.vertical_groups = []
        for index in range(9):
            data = [self.cells[i * 3 + j][index] for i in range(3) for j in range(3)]
            group_id = index
            self.vertical_groups.append(models.VerticalGroupModel(group_id, data))
        ## horizontal groups
        self.horizontal_groups = []
        for index in range(9):
            data = [self.cells[index][i * 3 + j] for i in range(3) for j in range(3)]
            group_id = index
            self.horizontal_groups.append(models.HorizontalGroupModel(group_id, data))
        ## cross groups
        self.cross_groups = []
        data = [self.cells[i + 3 * j][i + 3 * j] for i in range(3) for j in range(3)]
        self.cross_groups.append(models.CrossGroupModel(0, data))
        data = [self.cells[i + 3 * j][8 - (i + 3 * j)] for i in range(3) for j in range(3)]
        self.cross_groups.append(models.CrossGroupModel(1, data))
        self.status_model.turn_start()

    def update(self, init_data: List[List[int]]) -> None:
        """更新"""
        self.init_data = init_data
        for row_i, row_values in enumerate(init_data):
            for col_i, cell_value in enumerate(row_values):
                self.cells[row_i][col_i].set_value(cell_value)

        self.status_model.turn_start()

    def reset(self) -> None:
        """最初の状態(初期データ)に戻す"""
        self.update(self.init_data)

    def set_pazzle_group(self, group:List[List[int]]) -> None:
        """ジグソーグループを設定"""
        self.jigsaw_data = group

        self.pazzle_groups = []
        datas = [[] for _ in range(9)]
        for row, values  in enumerate(group):
            for col, value in enumerate(values):
                datas[value-1].append(self.cells[row][col])
        for group_id, data in enumerate(datas):
            self.pazzle_groups.append(models.PazzleGroupModel(group_id, data))


    def check_to_complete(self) -> bool:
        """数独を解き終わっているか確認する処理"""
        for row in self.cells:
            for cell in row:
                if cell.get_value() > 0:
                    pass
                else:
                    return False
        return True

    def get_init_data(self) -> List[List[int]]:
        """get init data"""
        return self.init_data

    def get_square_groups(self) -> List[models.SquareGroupModel]:
        """get square_groups"""
        return self.square_groups

    def get_vertical_groups(self) -> List[models.VerticalGroupModel]:
        """get vertical groups"""
        return self.vertical_groups

    def get_horizontal_groups(self) -> List[models.HorizontalGroupModel]:
        """get horizontal groups"""
        return self.horizontal_groups

    def get_cross_groups(self) -> List[models.CrossGroupModel]:
        """ get cross groups"""
        return self.cross_groups

    def get_jigsaw_groups(self) -> List[models.PazzleGroupModel]:
        """get jigsaw groups"""
        return self.pazzle_groups

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
                    for row_cells in self.cells:
                        for cell in row_cells:
                            if cell.get_row() == row and cell.get_group('square') != group_id:
                                cell.set_candidate(number, False)
                if col is not None:
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

    def compute_others_cross(self) -> None:
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

    def compute_others_pazzle(self) -> None:
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

    def check_pairs_in_group_normal(self) -> None:
        """check pairs in group normal"""
        for hgroup in self.horizontal_groups:
            hgroup.check_pairs_in_group()
        for vgroup in self.vertical_groups:
            vgroup.check_pairs_in_group()
        for sgroup in self.square_groups:
            sgroup.check_pairs_in_group()

    def check_pairs_in_group_cross(self) -> None:
        """check pairs in group normal"""
        for hgroup in self.horizontal_groups:
            hgroup.check_pairs_in_group()
        for vgroup in self.vertical_groups:
            vgroup.check_pairs_in_group()
        for sgroup in self.square_groups:
            sgroup.check_pairs_in_group()
        for cgroup in self.cross_groups:
            cgroup.check_pairs_in_group()

    def check_pairs_in_group_jigsaw(self) -> None:
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
