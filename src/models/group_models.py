# coding: utf-8
"""group models"""
from typing import List

import models


class BaseGroupModel:
    """BaseGroupModel"""
    group_name = 'base'

    def __init__(self, group_id:int, data:List[models.CellModel]):
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
