
class LoanPay:

    '''КЛАСС для расчета параметров переплаты по кредиту
    АРГУМЕНТЫ (получаемые при создании класса)
        loan        - сумма долга, денежная единица, +FLOAT/INT
        periods     - количество периодов выплаты кредита (месяцев, лет) + INTEGER XXX
        month       - являются ли периоды месяцами TRUE, или годами FALSE, BOOL
        interest    - ставка, % годовых, +FLOAT/INT
        inflate     - инфляция, % годовы, FLOAT/INT (может быть отрицательным значением)
        comiss      - ежемесячная комиссия, денежная единица, +FLOAT/INT
        insurance   - ежегодный платеж страхования, денежные единицы,   +FLOAT/INT
        decimal = 2 - число знаковых после запятой для свойств в денежных единицах, ОПЦИОНАЛЬНО, INT оптимально 0-3

    СОЗДАВАЕМЫЕ СВОЙСТВА-------------------------------------------------------------------------------------------
    Наличие ошибки во входящих параметрах или расчетах --------------------
        self.errors = True      - флаг свидетельствующий об  ошибке
        self.errmess = "Error message fixing stage where error occures"
    Успешное выполнение ---------------------------------------------------
        self.errors = False     - флаг свидетельствующий об отсутствии ошибки
        self.errmess = ""       - сообщение об ошибке - пустая строка
        self.rank               - числовая оценка качества кредита по шкале от 0 до 10
        self.interest_discounted        - используем для качественной тексто-цветовой оценки в хабе (
        self.overpaid_discounted_pc     - реальная переплата %
        self.overpaid               - переплата номинальная
        self.overpaid_discounted    - переплата реальная (с учетом инфляции)
        self.annuity                - аннуитетный платеж (с учетом ежемсячных комиссий)
        self.interest_effective     - эффективная % ставка по кредиту (с учетом комиссий)
        self.interest_over_inflate  - превышение эффективной ставки над инфляцией'''
      
    def __init__(self, loan, periods, is_month, interest, inflate, comiss, insurance, decimal=2):
        self.loan = loan
        #self.periods = periods
        self.__is_month = is_month
        self.interest = interest
        self.inflate = inflate
        self.comiss = comiss
        self.insurance = insurance
        self.decimal = decimal
        self.__periods = self.periods(self, periods)

        self.calculate(self)

    def calculate(self):
            years = self.__periods / 12  # срок кредита в годах
            inflate_month_abs = (1 + self.inflate / 100) ** (1 / 12) - 1
            interest_pc_per_month = self.interest / 100 / 12  # перевод годовых процентов в ежемесячные
            inflate_month_discount = 1 / (1 + inflate_month_abs)  # коэф. дисконтирования к предыдущему месяца
            payment_month = self.loan * (interest_pc_per_month + interest_pc_per_month /
                                    ((1 + interest_pc_per_month) ** self.__periods - 1)) + self.comiss
            payment_total = (payment_month + self.insurance / 12) * self.__periods  # добавляем ежегодный страховой платеж

             # Расчет дисконтированных денежных потоков
            payment_total_discount = 0  # инициируем переменную сумма всех платежей, дисконтированная
            for theperiod in range(1, self.__periods + 1):
                month_discount = inflate_month_discount ** theperiod  # коэффициент дисконтирования для текущего месяца
                payment_month_discount = payment_month * month_discount  # дисконтированный платеж в текущем месяце
                payment_total_discount += payment_month_discount  # суммируем дисконтированный результат

            overpaid = payment_total - self.loan  # переплата номинальная
            comiss_total = (self.comiss + self.insurance / 12) * self.periods  # суммарный размер уплаченных комиссий
            overpaid_discounted = payment_total_discount - self.loan  # переплата реальная (с учетом инфляции)
            overpaid_discounted_pc = overpaid_discounted / self.loan * 100  # переплата реальная , % от кредита

            comiss_abs = (1 + comiss_total / self.loan) ** (1 / years)  # размер комиссий по отношению к сумме долга, в долях
            comiss_pc = (comiss_abs - 1) * 100  # размер комиссий по отношению к сумме долга, в %
            interest_effective = self.interest + comiss_pc  # эффективная % ставка по кредиту (с учетом комиссий)

            eff_interest_discount_pc = interest_effective - self.inflate  # базовый параметр для оценки качества кредита
            rank = 10 - eff_interest_discount_pc  # инициируем оценку на осве базового показателя
            if rank < 0:  # в случае превышения пороговых значений
                rank = 0  # корректируем велчину
            elif rank > 10:
                rank = 10
            # Оценку качества кредита и разбиение на категории на базе rank оставляем в модуле-хабе, т.к. там оформление
            # Для этого используем параметр interest_discounted
            # loan_quality_grade = ""  # число - индекс категории для оценки качества кредита
            # loan_quality_verb = ""  # вербальная оценка качества кредит
            # loan_quality_hint = ""  # дополнительная вербальная оценка качества кредит

            self.rank = round(rank, 1)  # числовая оценка качества кредита по шкале от 0 до 10
            self.interest_discounted = round(eff_interest_discount_pc, 1)  # используем для вербально-цветовой оценки
            self.overpaid_discounted_pc = round(overpaid_discounted_pc, 1)  # реальная переплата %
            self.overpaid = round(overpaid, self.decimal)  # переплата номинальная
            self.overpaid_discounted = round(overpaid_discounted, self.decimal)  # переплата реальная (с учетом инфляции)
            self.annuity = round(payment_month, self.decimal)  # аннуитетный платеж (с учетом ежемсячных комиссий)
            self.interest_effective = round(interest_effective,
                                            1)  # эффективная % ставка по кредиту (с учетом комиссий)
            self.interest_over_inflate = round(eff_interest_discount_pc,
                                               1)  # превышение эффективной ставки над инфляцией

    
    
    
    @property
    def periods(self):
        return self.__periods

    @periods.setter
    def periods(self, value):
        '''если выбран годовой формат данных, умножаем количество месяцев'''
        if not self.__is_month:
            self.__periods = value * 12
        else:
            self.__periods = value

    @property
    def month(self):
        return self.__is_month

    @month.setter
    def month(self, value):
        self.__is_month = value
        self.periods(self, self.__periods)