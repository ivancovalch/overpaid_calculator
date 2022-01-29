
import locale
from kivy.config import Config

#Config.set('modules', 'screen', 'onex')
#Config.set('graphics', 'width', '540')
#Config.set('graphics', 'height', '960')


from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import StringProperty


import views


if (platform != 'android' ):
    Config.set("graphics", 'fullscreen', 0)
    Window.size = (540, 960)
    Window.fullscreen = False
    Window.top = 30

Builder.load_file('views.kv')

class OverPaidCalculatorApp(MDApp):

    locale = StringProperty()
    currency = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.locale = 'RU_ru'
        self.currency = 'RUB'
        locale.setlocale(locale.LC_ALL, '')
        # if platform in 'android':
        #     from jnius import autoclass
        #     Locale = autoclass('java.util.Locale')
        #     Currency = autoclass('java.util.Currency')
        #     jobj_locale = Locale.getDefault(Locale.Category.DISPLAY)
        #     self.locale = jobj_locale.toLanguageTag()
        #     self.currency = Currency.getDisplayName(jobj_locale)


    def build(self):

        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"

        return views.Container()

if __name__ == "__main__":
    OverPaidCalculatorApp().run()