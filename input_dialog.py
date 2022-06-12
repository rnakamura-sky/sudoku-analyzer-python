# coding: utf-8
"""input dialog module"""
import wx

import utils

class InputDialog(wx.Dialog):
    """Input Dialog"""
    def __init__(self, *args, init_value:str=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.result = False

        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        if init_value is not None:
            self.text.SetValue(init_value)
        button = wx.Button(self, wx.ID_YES, 'OK')
        self.Bind(wx.EVT_BUTTON, self.click_button, button)

        font =  wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.text.SetFont(font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, 1, wx.EXPAND)
        sizer.Add(button, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def get_text(self):
        """get text"""
        return self.text.GetValue()

    def click_button(self, _):
        """click button"""
        _text = self.get_text()
        if utils.check_input_data(_text):
            utils.string2data(_text)

            self.result = True
            self.Close(True)
            return True
        else:
            wx.MessageBox(
                message='データの形式が誤っています。',
            )
            return False

    def get_result(self):
        """get result"""
        return self.result
