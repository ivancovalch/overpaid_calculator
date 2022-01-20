import os

from kivy.config import Config

Config.set("graphics", 'fullscreen', 0)
#Config.set('modules', 'screen', 'onex')
#Config.set('graphics', 'width', '540')
#Config.set('graphics', 'height', '960')


from kivymd.app import MDApp
from kivy.lang import Builder, Parser
from kivy.core.window import Window
from kivy.utils import platform

from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import Screen
from kivymd.uix.card import MDCard
from kivymd.color_definitions import colors
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, DictProperty

import models
import views
from calcl import LoanPay as Lp


if (platform != 'android' ):
    Window.size = (540, 960)

Builder.load_file('views.kv')


def print_hi():
    loan = 100000
    periods = 5
    month = False
    interest = 11
    inflate = 8.6
    comiss = 20
    insurance = 100
    decimal = 2

    lpcur = Lp(loan, periods, month, interest, inflate, comiss, insurance, decimal)

    print(lpcur.__dict__)

class OverPaidCalculatorApp(MDApp):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def build(self):

        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"

        return views.Container()

if __name__ == "__main__":
    OverPaidCalculatorApp().run()