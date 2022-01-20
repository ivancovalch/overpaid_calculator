
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.popup import Popup

from kivymd.color_definitions import colors

from kivy.properties import StringProperty

class Container(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

