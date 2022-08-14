# coding: utf-8
"""セルパネル"""
import wx


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
