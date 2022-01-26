from kivy.app import App
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.textfield import MDTextFieldRect
from kivy.properties import StringProperty, ColorProperty, NumericProperty

from calcl import LoanPay

class Container(Screen):

    lp = LoanPay(1000000, 12, True, 10, 8, 0, 0)

    quality = StringProperty()
    quality_hint = StringProperty()
    quality_color = ColorProperty()
    money_back_bar_size = NumericProperty(1)
    money_over_bar_size = NumericProperty()
    overpaid_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.loan.text = "1000000"
        self.ids.periods.text = "12"
        self.ids.interest.text = "10"
        self.ids.inflate.text = "8"
        self.ids.comiss.text = "0"
        self.ids.insurance.text = "0"


        self.lp.bind(interest_over_inflate = self.set_quality)
        self.lp.bind(overpaid_discounted_pc = self.set_overpaid)
        self.lp.bind(rank = self.set_stars)
        self.set_quality(None, 2)
        self.set_overpaid(None,None)
        self.set_stars(None, 8)

        self.lp.calculate()

    def validate_checkbox(self):
        if self.ids.cb_month.active:
            self.lp.is_month = True
        if self.ids.cb_year.active:
            self.lp.is_month = False

        try:
            self.lp.calculate()
        except:
            pass

    def set_quality(self, obj, val):
        val = float(val)
        if val < 0:
            self.quality = "Подозрительно отлично!"
            self.quality_hint = "Банк теряет на вас деньги"
            # темно-зеленый
            self.quality_color = [0, .7, 0, 1]
        elif val < 2.5:
            self.quality = "Очень хорошо"
            self.quality_hint = "Небольшая переплата "
            # желто-зеленый 173,255,47
            self.quality_color = [173/255, 1, 47/255, 1]
        elif val < 5:
            self.quality = "Средне"
            self.quality_hint = "Обычные для рынка условия "
            # желтый
            self.quality_color = [.9, .7, .2, 1]
        elif val <= 8:
            self.quality = "Плохенько"
            self.quality_hint = "Дорогой кредит"
            # оранжевый
            self.quality_color = [1, .5, 0, 1]
        elif val > 8:
            self.quality = "Ужасно"
            self.quality_hint = "Очень дорогой кредит"
            # темно-красный
            self.quality_color = [.9, 0.1, 0.1, 1]

        # Модификация вида виджетов в зависимости от полученного результата
        widg_maincol = ['lb_annuity_text', 'lb_annuity','lb_loanoverpaid_text', 'lb_loanoverpaid', 'lb_money_back',
                        'lb_money_over','lb_results', 'lb_efinterest_text', 'lb_efinterest', 'lb_efinterest_infl_text',
                        'lb_efinterest_infl'] # список виджетов, которые необходимо модифицировать исходя из качества
        for thewidget in widg_maincol:
            self.ids[thewidget].text_color = self.quality_color


    def set_overpaid(self, obj, val):
        self.money_back_bar_size = (100 - float(self.lp.overpaid_discounted_pc)) / 100
        self.money_over_bar_size = float(self.lp.overpaid_discounted_pc) - 100
        overpaid_discounted_to_scale = float(self.lp.overpaid_discounted)
        if overpaid_discounted_to_scale > 0:
            self.overpaid_color = [1, .3, .1, 1]
        else:
            self.overpaid_color = [.1, .7, .1, 1]
            overpaid_discounted_to_scale = - overpaid_discounted_to_scale # для формирования шкалы нужны положительные величины

        # Расчет размера шкалы и его элементов
        total_scale_length = overpaid_discounted_to_scale + self.lp.loan # шкала = тело долга + переплаты
        self.money_back_bar_size = self.lp.loan / total_scale_length  # делим для нормализации (приводим к долям целого)
        self.money_over_bar_size = overpaid_discounted_to_scale / total_scale_length
        print(f"overpaid_discounted_to_scale {overpaid_discounted_to_scale}")
        print(f"total_scale_length {total_scale_length}")
        print(f"loan {self.lp.loan}")

        # Устанавливаем цветовые значения виджетов шкалы в зависимости от знака переплаты
        self.ids.lb_money_over.md_bg_color =  self.overpaid_color
        for thewidget in ['lb_loanoverpaidiscpc', 'lb_loanoverpaidisc_text', 'lb_loanoverpaidisc']:
            self.ids[thewidget].text_color = self.overpaid_color


    def set_stars(self, obj, val):
        val = float(val)
        for i , star in enumerate(self.ids.stars.children[::-1], start=1):
            if i - val < 0.9:
                star.icon = "star"
            elif i - val <= 0:
                star.icon = "star-half-full"
            else:
                star.icon = "star-outline"

class TFbase(MDTextField):  # MDTextField

    name = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_focus(self, instance, value, *largs):
        root = App.get_running_app().root
        if root is None:
            return super().on_focus(instance, value, *largs)

        self.validate(root)
        return super().on_focus(instance, value, *largs)

    def validate(self, root):
            instance = self
            name = self.name

            if instance.focus:
                return

            if not instance.text:
                instance.text = str(getattr(root.lp, name))

            if len(instance.text) > instance.max_text_length:
                instance.error = True
                return
            else:
                instance.error = False

            try:
                if 'int' in instance.input_filter:
                    val = (int)(instance.text)
                else:
                    val = (float)(instance.text)
            except:
                instance.error = True

            if str(name) not in ('comiss', 'insurance', 'inflate') and val <= 0:
                instance.error = True
                return
            elif str(name) is not 'inflate' and val < 0:
                instance.error = True
                return
            else:
                instance.error = False

            setattr(root.lp, name, val)

            try:
                root.lp.calculate()
            except:
                instance.error = True

    def clear_text(self):
        if self.focus:
            self.text = ''
