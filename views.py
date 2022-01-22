
from kivymd.uix.screen import Screen

from calcl import LoanPay

class Container(Screen):

    lp = LoanPay(1000000, 12, True, 10, 8, 0, 0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.loan.text = "1000000"
        self.ids.ti_periods.text = "12"
        self.ids.ti_interest.text = "10"
        self.ids.ti_inflate.text = "8"
        self.ids.ti_comiss.text = "0"
        self.ids.ti_insurance.text = "0"


    def validate_loan(self, instance):
        if instance.focus == True:
            return

        val = (int)(instance.text)
        if val <= 0:
            instance.error = True
            return
        else:
            instance.error = False
        self.lp.loan = val

        try:
            self.lp.calculate()
        except:
            instance.error = True

    def validate_periods(self, instance):
        if instance.focus == True:
            return

        val = (int)(instance.text)
        if val <= 0:
            instance.error = True
            return
        else:
            instance.error = False
        self.lp.periods = val

        try:
            self.lp.calculate()
        except:
            instance.error = True

    def validate_percent(self, instance):
        if instance.focus == True:
            return

        val = (float)(instance.text)
        if val <= 0:
            instance.error = True
            return
        else:
            instance.error = False
        self.lp.interest = val

        try:
            self.lp.calculate()
        except:
            instance.error = True

    def validate_inflate(self, instance):
        if instance.focus == True:
            return

        val = (float)(instance.text)
        if val <= 0:
            instance.error = True
            return
        else:
            instance.error = False
        self.lp.inflate = val

        try:
            self.lp.calculate()
        except:
            instance.error = True

    def validate_comiss(self, instance):
        if instance.focus == True:
            return

        val = (float)(instance.text)
        if val < 0:
            instance.error = True
            return
        else:
            instance.error = False
        self.lp.comiss = val

        try:
            self.lp.calculate()
        except:
            instance.error = True

    def validate_insurance(self, instance):
        if instance.focus == True:
            return

        val = (float)(instance.text)
        if val < 0:
            instance.error = True
            return
        else:
            instance.error = False
        self.lp.insurance = val

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
        





