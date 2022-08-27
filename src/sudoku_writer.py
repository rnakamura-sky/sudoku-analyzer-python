# coding: utf-8

"""数独保存用モジュール"""
import pathlib
import utils
from typing import List


def write(type_name:str, data:List[List[int]], jigsaw_data=None):
    """write"""
    file_path = pathlib.Path(__file__)
    base_folder_path = file_path.parent.parent / 'questions'
    base_folder_path = base_folder_path.absolute()
    folder_path = base_folder_path / type_name

    number = -1
    # for num in range(1, 1000):
    for num in range(1, 100):
        file_pattern = f'{type_name}_{str(num).zfill(3)}*.txt'
        # print(file_pattern)
        if len(list(folder_path.glob(file_pattern))) > 0:
            # print('exist')
            pass
        else:
            # print('ok')
            number = num
            break
    file_name = f'{type_name}_{str(number).zfill(3)}.txt'
    file_path = folder_path / file_name
    print(file_path)
    
    with open(file_path, mode='w', encoding='utf-8') as file:
        string_data = utils.data2string(data)
        file.writelines(string_data)

        if type_name == 'jigsaw':
            file.write('\n')
            file.write('\n')
            string_jigsaw = utils.data2string(jigsaw_data)
            file.writelines(string_jigsaw)
    return file_name

if __name__ == '__main__':
    print('Hello world')
    data = [
        [1,2,3,4,5,6,7,8,9],
        [1,2,3,4,5,6,7,8,9],
        [1,2,3,4,5,6,7,8,9],
        [1,2,3,4,5,6,7,8,9],
        [1,2,3,4,5,6,7,8,9],
        [1,2,3,4,5,6,7,8,9],
        [1,2,3,4,5,6,7,8,9],
        [1,2,3,4,5,6,7,8,9],
        [1,2,3,4,5,6,7,8,9],
    ]
    write('normal', data, None)