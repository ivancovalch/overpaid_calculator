
from kivymd.uix.screen import Screen

from calcl import LoanPay

class Container(Screen):

    lp = LoanPay(1000000, 12, True, 10, 8, 0, 0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.loan.text = "1000000"
        self.ids.periods.text = "12"
        self.ids.interest.text = "10"
        self.ids.inflate.text = "8"
        self.ids.comiss.text = "0"
        self.ids.insurance.text = "0"


    def validate(self, name):
        instance = self.ids[name]
        if instance.focus is True:
            return
        
        if 'int' in instance.input_filter:
            val = (int)(instance.text)
        else:
            val = (float)(instance.text)
        if name in ('comiss', 'insurance') and val < 0:
            instance.error = True
            return
        elif val <= 0:
            instance.error = True
            return
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
        





