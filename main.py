# coding: utf-8
""" Sudoku """
import wx

from model import DataModel
from input_dialog import InputDialog
import utils

class CellPanel(wx.Panel):
    """CellView"""
    def __init__(self, cell_model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cell_model = cell_model
        # content
        self.value = self.cell_model.get_display_value()
        self.is_visible = True
        if self.value:
            self.candidates = [False for _ in range(9)]
        else:
            self.candidates = [True for _ in range(9)]

        self.text_font = wx.Font(
            20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.candidate_font = wx.Font(
            9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.active_color = wx.BLACK
        self.deactive_color = wx.LIGHT_GREY

        # view
        self.text_panel = wx.Panel(
            parent=self,
            id=wx.ID_ANY)
        self.text = wx.StaticText(
            parent=self.text_panel,
            id=wx.ID_ANY,
            label=self.value
        )
        self.text.SetFont(self.text_font)

        self.candidate_panel = wx.Panel(
            parent=self,
            id = wx.ID_ANY
        )
        self.candidate_1 = wx.StaticText(parent=self.candidate_panel, id=wx.ID_ANY, label='1')
        self.candidate_2 = wx.StaticText(parent=self.candidate_panel, id=wx.ID_ANY, label='2')
        self.candidate_3 = wx.StaticText(parent=self.candidate_panel, id=wx.ID_ANY, label='3')
        self.candidate_4 = wx.StaticText(parent=self.candidate_panel, id=wx.ID_ANY, label='4')
        self.candidate_5 = wx.StaticText(parent=self.candidate_panel, id=wx.ID_ANY, label='5')
        self.candidate_6 = wx.StaticText(parent=self.candidate_panel, id=wx.ID_ANY, label='6')
        self.candidate_7 = wx.StaticText(parent=self.candidate_panel, id=wx.ID_ANY, label='7')
        self.candidate_8 = wx.StaticText(parent=self.candidate_panel, id=wx.ID_ANY, label='8')
        self.candidate_9 = wx.StaticText(parent=self.candidate_panel, id=wx.ID_ANY, label='9')

        self.candidate_texts = [
            self.candidate_1,
            self.candidate_2,
            self.candidate_3,
            self.candidate_4,
            self.candidate_5,
            self.candidate_6,
            self.candidate_7,
            self.candidate_8,
            self.candidate_9,
        ]

        # layout
        self.layout = wx.BoxSizer()
        self.SetSizer(self.layout)

        text_layout = wx.GridSizer(rows=1, cols=1, gap=(0, 0))
        text_layout.Add(self.text, flag=wx.ALIGN_CENTER)
        self.text_panel.SetSizer(text_layout)

        candidate_layout = wx.GridSizer(rows=3, cols=3, gap=(0, 0))
        candidate_layout.Add(self.candidate_1, proportion=1, flag=wx.ALIGN_CENTER)
        candidate_layout.Add(self.candidate_2, proportion=1, flag=wx.ALIGN_CENTER)
        candidate_layout.Add(self.candidate_3, proportion=1, flag=wx.ALIGN_CENTER)
        candidate_layout.Add(self.candidate_4, proportion=1, flag=wx.ALIGN_CENTER)
        candidate_layout.Add(self.candidate_5, proportion=1, flag=wx.ALIGN_CENTER)
        candidate_layout.Add(self.candidate_6, proportion=1, flag=wx.ALIGN_CENTER)
        candidate_layout.Add(self.candidate_7, proportion=1, flag=wx.ALIGN_CENTER)
        candidate_layout.Add(self.candidate_8, proportion=1, flag=wx.ALIGN_CENTER)
        candidate_layout.Add(self.candidate_9, proportion=1, flag=wx.ALIGN_CENTER)
        self.candidate_panel.SetSizer(candidate_layout)

        # debug color
        self.SetBackgroundColour(wx.YELLOW)
        self.text_panel.SetBackgroundColour(wx.GREEN)
        self.candidate_panel.SetBackgroundColour(wx.CYAN)

        # show
        self.on_show()

    def set_candidates_color(self):
        """show candidates"""
        for candidate_text, candidate_value in zip(self.candidate_texts, self.candidates):
            if candidate_value:
                candidate_text.SetForegroundColour(self.active_color)
            else:
                candidate_text.SetForegroundColour(self.deactive_color)

    def on_show(self):
        """show"""
        # debug print
        # print(self, '[' + self.value + ']')
        if self.value:
            self.candidate_panel.Hide()
            self.layout.Clear()
            self.layout.Add(self.text_panel, flag=wx.EXPAND, proportion=1)
            self.text_panel.Show()
        else:
            self.text_panel.Hide()
            self.layout.Clear()
            if self.is_visible:
                self.layout.Add(self.candidate_panel, flag=wx.EXPAND, proportion=1)
                self.set_candidates_color()
                self.candidate_panel.Show()
            else:
                self.candidate_panel.Hide()
        self.SendSizeEvent()
        self.Refresh()

    def set_show_mode(self):
        """set show mode"""
        self.is_visible = not self.is_visible
        self.on_show()

    def set_value(self, value):
        """set value"""
        self.value = value
        self.text.SetLabel(self.value)

    def set_candidate(self, number, candidate: bool):
        """set candidate"""
        self.candidates[number - 1] = candidate
        color = self.active_color if candidate else self.deactive_color
        self.candidate_texts[number - 1].SetForegroundColour(color)

    def update_numbers(self):
        """update numbers"""
        new_value = self.cell_model.get_display_value()
        if new_value == self.value:
            new_candidates = self.cell_model.get_candidates()
            for index in range(9):
                current_candidate = self.candidates[index]
                new_candidate = new_candidates[index]
                if current_candidate == new_candidate:
                    pass
                else:
                    self.set_candidate(index + 1, new_candidate)
        else:
            self.value = new_value
            self.text.SetLabel(self.value)
            new_candidates = self.cell_model.get_candidates()
            for index in range(9):
                current_candidate = self.candidates[index]
                new_candidate = new_candidates[index]
                if current_candidate == new_candidate:
                    pass
                else:
                    self.set_candidate(index + 1, new_candidate)
            self.on_show()

    def set_cell_model(self, cell_model):
        """set cell model"""
        # debug print
        self.cell_model = cell_model


class SquarePanel(wx.Panel):
    """Square View"""
    def __init__(self, group_model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.group_model = group_model
        self.cell_models = group_model.get_cell_models()
        self.cells = [None for _ in range(9)]
        for cell_index in range(len(self.cells)):
            row_index = cell_index // 3
            col_index = cell_index % 3
            cell_model = self.cell_models[row_index][col_index] 
            self.cells[cell_index] = CellPanel(parent=self, cell_model=cell_model)

        # layout
        layout = wx.GridSizer(rows=3, cols=3, gap=(1, 1))
        for cell in self.cells:
            layout.Add(cell, proportion=1, flag=wx.EXPAND)
        self.SetSizer(layout)

        # debag color
        self.SetBackgroundColour(wx.BLUE)

    def set_show_mode(self):
        """set show mode"""
        for cell in self.cells:
            cell.set_show_mode()

    def update_numbers(self):
        """update numbers"""
        for cell in self.cells:
            cell.update_numbers()

    def set_group_model(self, group_model):
        """set group model"""
        self.group_model = group_model
        self.cell_models = group_model.get_cell_models()
        for cell_index in range(len(self.cells)):
            row_index = cell_index // 3
            col_index = cell_index % 3
            cell_model = self.cell_models[row_index][col_index] 
            self.cells[cell_index].set_cell_model(cell_model)


class Boad(wx.Panel):
    """"Boad"""
    def __init__(self, data_model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data_model = data_model
        self.square_group_models = data_model.get_square_groups()

        self.groups = [None for _ in range(9)]

        for group_index in range(len(self.groups)):
            row_group = group_index // 3
            col_group = group_index % 3

            group_model = self.square_group_models[row_group][col_group]
            self.groups[group_index] = SquarePanel(parent=self, id=wx.ID_ANY, group_model=group_model)

        # layout
        layout = wx.GridSizer(rows=3, cols=3, gap=(3, 3))
        for group in self.groups:
            layout.Add(group, proportion=1, flag=wx.EXPAND)
        self.SetSizer(layout)

        # debug color
        self.SetBackgroundColour(wx.BLACK)

    def set_show_mode(self):
        """set show mode"""
        for group in self.groups:
            group.set_show_mode()

    def update_numbers(self):
        """update numbers"""
        for group in self.groups:
            group.update_numbers()
        self.Update()
        self.Refresh()

    def update_data_model(self):
        """update data model"""
        self.square_group_models = self.data_model.get_square_groups()

        for group_index in range(len(self.groups)):
            row_group = group_index // 3
            col_group = group_index % 3

            group_model = self.square_group_models[row_group][col_group]
            self.groups[group_index].set_group_model(group_model)


class MainFrame(wx.Frame):
    """MainFrame"""
    def __init__(self, data_model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data_model = data_model

        self.base_panel = wx.Panel(
            parent=self,
            id=wx.ID_ANY
        )

        ## main panel
        self.main_panel = wx.Panel(
            parent=self.base_panel,
            id=wx.ID_ANY
        )
        self.main_component = Boad(
            parent=self.main_panel,
            id=wx.ID_ANY,
            data_model=data_model
        )
        status_text = 'Status: '
        status_text += 'Completed' if self.data_model.check_to_complete() else 'Uncompleted'
        self.status_label = wx.StaticText(
            parent=self.main_panel,
            id=wx.ID_ANY,
            label=status_text
        )

        ## side panel
        self.side_panel = wx.Panel(
            parent=self.base_panel,
            id=wx.ID_ANY,
        )
        self.side_button = wx.Button(
            parent=self.side_panel,
            label='Change show mode'
        )

        ### side panel button
        self.select_button = wx.Button(
            parent=self.side_panel,
            label='候補が絞られているものを選択'
        )
        self.select_in_square_button = wx.Button(
            parent=self.side_panel,
            label='正方形内で候補が絞られているものを選択'
        )
        self.select_in_vertical_button = wx.Button(
            parent=self.side_panel,
            label='縦列で候補が絞られているものを選択'
        )
        self.select_in_horizontal_button = wx.Button(
            parent=self.side_panel,
            label='横列で候補が絞られているものを選択'
        )
        self.compute_button_1 = wx.Button(
            parent=self.side_panel,
            label='正方形内での候補計算'
        )
        self.compute_button_2 = wx.Button(
            parent=self.side_panel,
            label='横グループでの候補計算'
        )
        self.compute_button_3 = wx.Button(
            parent=self.side_panel,
            label='縦グループでの候補計算'
        )
        self.compute_auto_button = wx.Button(
            parent=self.side_panel,
            label='全自動計算'
        )
        self.side_panel.SetBackgroundColour(wx.BLACK)

        # Layout
        ## main
        main_layout = wx.BoxSizer(wx.VERTICAL)
        main_layout.Add(self.main_component, flag=wx.EXPAND,proportion=1)
        main_layout.Add(self.status_label, flag=wx.EXPAND)
        self.main_panel.SetSizer(main_layout)

        ## side
        side_layout = wx.BoxSizer(orient=wx.VERTICAL)
        side_layout.Add(self.side_button, flag=wx.EXPAND)
        side_layout.Add(self.select_button, flag=wx.EXPAND)
        side_layout.Add(self.select_in_square_button, flag=wx.EXPAND)
        side_layout.Add(self.select_in_vertical_button, flag=wx.EXPAND)
        side_layout.Add(self.select_in_horizontal_button, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_1, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_2, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_3, flag=wx.EXPAND)
        side_layout.Add(self.compute_auto_button, flag=wx.EXPAND)
        self.side_panel.SetSizer(side_layout)

        ## base
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.main_panel, flag=wx.EXPAND, proportion=1)
        layout.Add(self.side_panel)
        self.base_panel.SetSizer(layout)

        ## menu
        # パネルを配置してからでないとうまく表示されないため、他のsizerがセットされたあとに
        # メニューを追加
        menu = wx.Menu()
        menu.AppendSeparator()
        menu_init = menu.Append(1, '初期状態に戻す')
        menu_create = menu.Append(2, '新しい問題を設定')
        menu_update = menu.Append(3, '問題を修正')
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, 'メニュー')
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_reset, menu_init)
        self.Bind(wx.EVT_MENU, self.on_initialize_from_dialog, menu_create)
        self.Bind(wx.EVT_MENU, self.on_update_data, menu_update)

        # Event
        self.side_button.Bind(
            event=wx.EVT_BUTTON, handler=self.click_button)
        self.select_button.Bind(
            event=wx.EVT_BUTTON, handler=self.click_select_button)
        self.select_in_square_button.Bind(
            event=wx.EVT_BUTTON, handler=self.click_select_in_square_button)
        self.select_in_vertical_button.Bind(
            event=wx.EVT_BUTTON, handler=self.click_select_in_vertical_button)
        self.select_in_horizontal_button.Bind(
            event=wx.EVT_BUTTON, handler=self.click_select_in_horizontal_button)
        self.compute_button_1.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_1)
        self.compute_button_2.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_2)
        self.compute_button_3.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_3)
        self.compute_auto_button.Bind(
            event=wx.EVT_BUTTON, handler=self.click_auto_compute_button)

    def click_button(self, _):
        """click button"""
        self.main_component.set_show_mode()

    def update_status(self):
        """update status"""
        status_text = 'Status: '
        status_text += 'Completed' if self.data_model.check_to_complete() else 'Uncompleted'
        status_text += '  '
        status_text += 'Changed' if self.data_model.is_changed() else 'No Changed'
        self.status_label.SetLabel(status_text)

    def click_select_button(self, _):
        """click select button"""
        self.data_model.start_turn()
        self.data_model.select_from_candidate()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to select')

    def click_select_in_square_button(self, _):
        """click select button"""
        self.data_model.start_turn()
        self.data_model.select_from_candidate_in_square()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to select in square')

    def click_select_in_vertical_button(self, _):
        """click select button"""
        self.data_model.start_turn()
        self.data_model.select_from_candidate_in_vertical()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to select in vertical')

    def click_select_in_horizontal_button(self, _):
        """click select button"""
        self.data_model.start_turn()
        self.data_model.select_from_candidate_in_horizontal()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to select in horizontal')

    def click_compute_button_1(self, _):
        """click compute button1"""
        self.data_model.start_turn()
        self.data_model.compute_square_candidate()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 1')

    def click_compute_button_2(self, _):
        """click compute button2"""
        self.data_model.start_turn()
        self.data_model.compute_horizontal_candidate()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 2')

    def click_compute_button_3(self, _):
        """click compute button3"""
        self.data_model.start_turn()
        self.data_model.compute_vertical_candidate()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 3')

    def click_auto_compute_button(self, _):
        """click auto compute button"""
        self.data_model.start_turn()
        count = 0
        while not self.data_model.check_to_complete():
            count += 1
            self.data_model.compute_square_candidate()
            self.data_model.compute_horizontal_candidate()
            self.data_model.compute_vertical_candidate()
            self.data_model.select_from_candidate()
            while True:
                self.data_model.start_turn()
                self.data_model.select_from_candidate_in_square()
                if not self.data_model.is_changed():
                    break
            while True:
                self.data_model.start_turn()
                self.data_model.select_from_candidate_in_vertical()
                if not self.data_model.is_changed():
                    break
            while True:
                self.data_model.start_turn()
                self.data_model.select_from_candidate_in_horizontal()
                if not self.data_model.is_changed():
                    break

            # TODO 現在の処理でクリアできない可能性が0でないため、50を上限として処理を終了させる
            if count >= 50:
                break

        self.main_component.update_numbers()
        self.update_status()
        print('complete to auto computed')
        print(f'Turn Count: {count}')

    def on_reset(self, _):
        """元の初期状態に戻す"""
        self.data_model.reset()
        self.update_data_model()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to reset')

    def on_initialize_from_dialog(self, _):
        """ダイアログで新しいデータをセット"""
        dialog = InputDialog(
            parent=None,
            id=wx.ID_ANY,
            title='Title',
            size=(300, 340)
        )
        dialog.ShowModal()
        result = dialog.get_result()
        if result:
            data = dialog.get_text()
            data = utils.string2data(data)
            self.data_model.initialize(data)
            self.update_data_model()
            self.main_component.update_numbers()
            self.update_status()
            print('Input')
        else:
            print('Cancel')
        dialog.Destroy()

    def on_update_data(self, _):
        """on update data"""
        str_data = utils.data2string(self.data_model.get_init_data())
        dialog = InputDialog(
            init_value=str_data,
            parent=None,
            id=wx.ID_ANY,
            title='Title',
            size=(300, 340)
        )
        dialog.ShowModal()
        result = dialog.get_result()
        if result:
            data = dialog.get_text()
            data = utils.string2data(data)
            self.data_model.initialize(data)
            self.update_data_model()
            self.main_component.update_numbers()
            self.update_status()
            print('Input')
        else:
            print('Cancel')
        dialog.Destroy()

    def update_data_model(self):
        """update data model"""
        self.main_component.update_data_model()


def main():
    """Main"""
    # Data
    # 設定する時のテンプレートとして使用してください。
    base_data = [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
    ]

    # 各列を数字のみの文字列で設定します。
    # 空白は0として設定します。
    base_data = [
        '000000007',
        '026750039',
        '000009010',
        '600000003',
        '000060408',
        '400000070',
        '042900001',
        '360020084',
        '580040300',
    ]
    base_data = [[int(value) for value in list(row)] for row in base_data]
    base_data = [[int(v) for v in list(row)] for row in base_data]
    data_model = DataModel(base_data)

    # debug print
    # print(data)

    # View
    app = wx.App()
    coordinate = wx.Point(10, 50)
    frame = MainFrame(
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
