# coding: utf-8
"""main frame"""
import wx

import utils
import sudoku_writer

import views
from views.input_dialog import InputDialog, GroupInputDialog


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
        self.main_component = views.Boad(
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
        self.select_in_cross_button = wx.Button(
            parent=self.side_panel,
            label='クロスで候補が絞られているものを選択'
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
        self.compute_button_4 = wx.Button(
            parent=self.side_panel,
            label='クロスグループでの候補計算'
        )
        self.compute_button_5 = wx.Button(
            parent=self.side_panel,
            label='SquareグループとCellとの関係'
        )
        self.compute_button_6 = wx.Button(
            parent=self.side_panel,
            label='PazzleグループとCellとの関係'
        )
        self.compute_button_7 = wx.Button(
            parent=self.side_panel,
            label='普通のナンプレ候補が二つの処理'
        )
        self.compute_button_8 = wx.Button(
            parent=self.side_panel,
            label='クロスのナンプレ候補が二つの処理'
        )
        self.compute_button_9 = wx.Button(
            parent=self.side_panel,
            label='ジグソーのナンプレ候補が二つの処理'
        )
        self.compute_button_10 = wx.Button(
            parent=self.side_panel,
            label='スクエアが決まる候補の処理'
        )
        self.compute_button_11 = wx.Button(
            parent=self.side_panel,
            label='スクエアが決まる候補の処理(クロス)'
        )
        self.compute_button_12 = wx.Button(
            parent=self.side_panel,
            label='スクエアが決まる候補の処理(ジグソー)'
        )

        self.compute_auto_button = wx.Button(
            parent=self.side_panel,
            label='全自動計算'
        )
        self.compute_auto_cross_button = wx.Button(
            parent=self.side_panel,
            label='全自動計算(クロス)'
        )
        self.compute_auto_pazzle_button = wx.Button(
            parent=self.side_panel,
            label='全自動計算(ジグソー)'
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
        side_layout.Add(self.select_in_cross_button, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_1, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_2, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_3, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_4, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_5, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_6, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_7, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_8, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_9, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_10, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_11, flag=wx.EXPAND)
        side_layout.Add(self.compute_button_12, flag=wx.EXPAND)
        side_layout.Add(self.compute_auto_button, flag=wx.EXPAND)
        side_layout.Add(self.compute_auto_cross_button, flag=wx.EXPAND)
        side_layout.Add(self.compute_auto_pazzle_button, flag=wx.EXPAND)
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
        menu_create_pazzle = menu.Append(4, 'ジグソーグループを設定')
        menu_update_pazzle = menu.Append(5, 'ジグソーグループを修正')
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, 'メニュー')
        self.Bind(wx.EVT_MENU, self.on_reset, menu_init)
        self.Bind(wx.EVT_MENU, self.on_initialize_from_dialog, menu_create)
        self.Bind(wx.EVT_MENU, self.on_update_data, menu_update)
        self.Bind(wx.EVT_MENU, self.on_create_pazzle_group, menu_create_pazzle)
        self.Bind(wx.EVT_MENU, self.on_update_pazzle_group, menu_update_pazzle)

        # 保存用メニュー
        menu_writer = wx.Menu()
        menu_writer.AppendSeparator()
        menu_write_normal = menu_writer.Append(6, 'ノーマルの保存')
        menu_write_cross = menu_writer.Append(7, 'クロスの保存')
        menu_write_jigsaw = menu_writer.Append(8, 'ジグソーの保存')
        self.Bind(wx.EVT_MENU, self.write_normal, menu_write_normal)
        self.Bind(wx.EVT_MENU, self.write_cross, menu_write_cross)
        self.Bind(wx.EVT_MENU, self.write_jigsaw, menu_write_jigsaw)
        menu_bar.Append(menu_writer, '書込')
        
        self.SetMenuBar(menu_bar)

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
        self.select_in_cross_button.Bind(
            event=wx.EVT_BUTTON, handler=self.click_select_in_cross_button)
        self.compute_button_1.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_1)
        self.compute_button_2.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_2)
        self.compute_button_3.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_3)
        self.compute_button_4.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_4)
        self.compute_button_5.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_5)
        self.compute_button_6.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_6)
        self.compute_button_7.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_7)
        self.compute_button_8.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_8)
        self.compute_button_9.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_9)
        self.compute_button_10.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_10)
        self.compute_button_11.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_11)
        self.compute_button_12.Bind(
            event=wx.EVT_BUTTON, handler=self.click_compute_button_12)
        self.compute_auto_button.Bind(
            event=wx.EVT_BUTTON, handler=self.click_auto_compute_button)
        self.compute_auto_cross_button.Bind(
            event=wx.EVT_BUTTON, handler=self.click_auto_cross_compute_button)
        self.compute_auto_pazzle_button.Bind(
            event=wx.EVT_BUTTON, handler=self.click_auto_pazzle_compute_button)

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

    def click_select_in_cross_button(self, _):
        """click select in cross button"""
        self.data_model.start_turn()
        self.data_model.select_from_candidate_in_cross()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to select in cross')

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

    def click_compute_button_4(self, _):
        """click compute button4"""
        self.data_model.start_turn()
        self.data_model.compute_cross_candidate()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 4')

    def click_compute_button_5(self, _):
        """click compute button5"""
        self.data_model.start_turn()
        self.data_model.select_other_squares()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 5')

    def click_compute_button_6(self, _):
        """click compute button6"""
        self.data_model.start_turn()
        self.data_model.select_other_pazzles()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 6')

    def click_compute_button_7(self, _):
        """click compute button  7"""
        self.data_model.start_turn()
        self.data_model.check_pairs_square()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 7')

    def click_compute_button_8(self, _):
        """click compute button  8"""
        self.data_model.start_turn()
        self.data_model.check_pairs_cross()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 8')

    def click_compute_button_9(self, _):
        """click compute button  9"""
        self.data_model.start_turn()
        self.data_model.check_pairs_pazzle()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 9')

    def click_compute_button_10(self, _):
        """click compute button 10"""
        self.data_model.start_turn()
        self.data_model.compute_others_square()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 10')

    def click_compute_button_11(self, _):
        """click compute button 11"""
        self.data_model.start_turn()
        self.data_model.compute_others_cross()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 11')

    def click_compute_button_12(self, _):
        """click compute button 12"""
        self.data_model.start_turn()
        self.data_model.compute_others_pazzle()
        self.main_component.update_numbers()
        self.update_status()
        print('complete to compute button 12')

    def click_auto_compute_button(self, _):
        """click auto compute button"""
        self.data_model.start_turn()
        count = 0
        while not self.data_model.check_to_complete():
            count += 1
            self.data_model.compute_square_candidate()
            self.data_model.compute_horizontal_candidate()
            self.data_model.compute_vertical_candidate()
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

            self.data_model.select_other_squares()

            self.data_model.check_pairs_square()
            self.data_model.compute_others_square()
            self.data_model.check_pairs_in_group_normal()

            self.data_model.select_from_candidate()

            # TODO 現在の処理でクリアできない可能性が0でないため、50を上限として処理を終了させる
            if count >= 50:
                wx.MessageBox('問題を解くことができませんでした。')
                break

        self.main_component.update_numbers()
        self.update_status()
        print('complete to auto computed')
        print(f'Turn Count: {count}')

    def click_auto_cross_compute_button(self, _):
        """click auto cross compute button"""
        self.data_model.start_turn()
        count = 0
        while not self.data_model.check_to_complete():
            count += 1
            self.data_model.compute_square_candidate()
            self.data_model.compute_horizontal_candidate()
            self.data_model.compute_vertical_candidate()
            self.data_model.compute_cross_candidate()

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
            while True:
                self.data_model.start_turn()
                self.data_model.select_from_candidate_in_cross()
                if not self.data_model.is_changed():
                    break

            self.data_model.select_other_squares()

            self.data_model.check_pairs_cross()
            self.data_model.compute_others_cross()
            self.data_model.check_pairs_in_group_cross()

            self.data_model.select_from_candidate()

            # TODO 現在の処理でクリアできない可能性が0でないため、50を上限として処理を終了させる
            if count >= 50:
                wx.MessageBox('問題を解くことができませんでした。')
                break

        self.main_component.update_numbers()
        self.update_status()
        print('complete to auto computed')
        print(f'Turn Count: {count}')

    def click_auto_pazzle_compute_button(self, _):
        """click auto pazzle compute button"""
        self.data_model.start_turn()
        count = 0
        while not self.data_model.check_to_complete():
            count += 1
            # self.data_model.compute_square_candidate()
            self.data_model.compute_pazzle_candidate()
            self.data_model.compute_horizontal_candidate()
            self.data_model.compute_vertical_candidate()
            while True:
                self.data_model.start_turn()
                # self.data_model.select_from_candidate_in_square()
                self.data_model.select_from_candidate_in_pazzle()
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

            self.data_model.select_other_pazzles()

            self.data_model.check_pairs_pazzle()
            self.data_model.compute_others_pazzle()
            self.data_model.check_pairs_in_group_jigsaw()

            self.data_model.select_from_candidate()

            # TODO 現在の処理でクリアできない可能性が0でないため、50を上限として処理を終了させる
            if count >= 50:
                wx.MessageBox('問題を解くことができませんでした。')
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

    def on_create_pazzle_group(self, _):
        """on create pazzle group"""
        dialog = GroupInputDialog(
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
            self.data_model.set_pazzle_group(data)
            self.update_data_model()
            self.main_component.update_numbers()
            self.update_status()
            print('Input')
        else:
            print('Cancel')
        dialog.Destroy()

    def on_update_pazzle_group(self, _):
        """on update pazzle group"""

    def write_normal(self, _):
        """write normal"""
        file_name = sudoku_writer.write('normal', self.data_model.init_data)
        message = f'保存しました。[{file_name}]'
        wx.MessageBox(message)


    def write_cross(self, _):
        """write cross"""
        file_name = sudoku_writer.write('cross', self.data_model.init_data)
        message = f'保存しました。[{file_name}]'
        wx.MessageBox(message)


    def write_jigsaw(self, _):
        """write jigsaw"""
        file_name = sudoku_writer.write('jigsaw', self.data_model.init_data, self.data_model.jigsaw_data)
        message = f'保存しました。[{file_name}]'
        wx.MessageBox(message)

