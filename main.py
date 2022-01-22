from kivy.config import Config

Config.set("graphics", 'fullscreen', 0)
#Config.set('modules', 'screen', 'onex')
#Config.set('graphics', 'width', '540')
#Config.set('graphics', 'height', '960')


from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform

import views


if (platform != 'android' ):
    Window.size = (540, 960)

Builder.load_file('views.kv')

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