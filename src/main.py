# coding: utf-8
""" Sudoku """
import logging
import logging.handlers

import wx

from models import DataModel

import views

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

logger.info('TEST')

def main():
    """Main"""

    # 各列を数字のみの文字列で設定します。
    # 空白は0として設定します。
    base_data = [
        '000000024',
        '000610008',
        '001050006',
        '040000005',
        '000030080',
        '305000401',
        '008000002',
        '070000003',
        '000000090',
    ]
    base_data = [[int(value) for value in list(row)] for row in base_data]
    data_model = DataModel(base_data)

    # View
    app = wx.App()
    coordinate = wx.Point(10, 50)
    frame = views.MainFrame(
        parent=None,
        id=wx.ID_ANY,
        title='Application',
        size=(700, 500),
        pos=coordinate,
        data_model=data_model)
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == '__main__':
    main()
