
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
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

    def validate(self, name):
        instance = self.ids[name]
        #base_cls = instance.__class__.__bases__[0]
        #print(super(MDTextField, instance.__self__))
        if instance.focus is True:
            #instance.on_focus(None, True)
            return #super(MDTextField, instance.__self__).on_focus()
        
        if 'int' in instance.input_filter:
            val = (int)(instance.text)
        else:
            val = (float)(instance.text)
            
        if name in ('comiss', 'insurance') and val < 0:
            instance.error = True
            #instance.on_error(None, True)
            return
        elif val <= 0:
            instance.error = True
            #base_cls.on_error(instance, None, True)
            #print(instance)
            #instance.error(True)
            #return super()
        else:
            instance.error = False

        setattr(self.lp, name, val)

        try:
            self.lp.calculate()
        except:
            instance.error = True


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

    def set_overpaid(self, obj, val):
        self.money_back_bar_size = (100 - float(self.lp.overpaid_discounted_pc)) / 100
        self.money_over_bar_size = float(self.lp.overpaid_discounted_pc) - 100
        if float(self.lp.overpaid_discounted) > 0:
            self.overpaid_color = [0.8, 0, 0, 1]
        else:
            self.overpaid_color = [0, 0.8, 0, 1]

    def set_stars(self, obj, val):
        val = float(val)
        for i , star in enumerate(self.ids.stars.children[::-1], start=1):
            if i - val < 0.9:
                star.icon = "star"
            elif i - val <= 0:
                star.icon = "star-half-full"
            else:
                star.icon = "star-outline"

# class TFbase(MDTextField):

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#     def error(self, is_error):
#         print('hi')
#         self.super().on_error(None, is_error)







