# coding: utf-8
"""square panel"""
import wx

import views


class SquarePanel(wx.Panel):
    """Square View"""
    def __init__(self, group_model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.group_model = group_model
        self.cell_models = group_model.get_cell_models()
        self.cells = [None for _ in range(9)]
        for cell_index in range(len(self.cells)):
            cell_model = self.cell_models[cell_index] 
            self.cells[cell_index] = views.CellPanel(parent=self, cell_model=cell_model)

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
            cell_model = self.cell_models[cell_index] 
            self.cells[cell_index].set_cell_model(cell_model)
