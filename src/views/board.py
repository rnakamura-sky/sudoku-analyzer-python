# coding: utf-8
"""board"""
import wx

import views

class Boad(wx.Panel):
    """"Boad"""
    def __init__(self, data_model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data_model = data_model
        self.square_group_models = data_model.get_square_groups()

        self.groups = [None for _ in range(9)]

        for group_index in range(len(self.groups)):
            group_model = self.square_group_models[group_index]
            self.groups[group_index] = views.SquarePanel(parent=self, id=wx.ID_ANY, group_model=group_model)

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
            group_model = self.square_group_models[group_index]
            self.groups[group_index].set_group_model(group_model)
