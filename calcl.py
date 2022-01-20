# КЛАСС для расчета параметров переплаты по кредиту
# АРГУМЕНТЫ (получаемые при создании класса)
#       loan        - сумма долга, денежная единица, +FLOAT/INT
#       periods     - количество периодов выплаты кредита (месяцев, лет) + INTEGER XXX
#       month       - являются ли периоды месяцами TRUE, или годами FALSE, BOOL
#       interest    - ставка, % годовых, +FLOAT/INT
#       inflate     - инфляция, % годовы, FLOAT/INT (может быть отрицательным значением)
#       comiss      - ежемесячная комиссия, денежная единица, +FLOAT/INT
#       insurance   - ежегодный платеж страхования, денежные единицы,   +FLOAT/INT
#       decimal = 2 - число знаковых после запятой для свойств в денежных единицах, ОПЦИОНАЛЬНО, INT оптимально 0-3

# СОЗДАВАЕМЫЕ СВОЙСТВА-------------------------------------------------------------------------------------------
#   Наличие ошибки во входящих параметрах или расчетах --------------------
#       self.errors = True      - флаг свидетельствующий об  ошибке
#       self.errmess = "Error message fixing stage where error occures"
#   Успешное выполнение ---------------------------------------------------
#       self.errors = False     - флаг свидетельствующий об отсутствии ошибки
#       self.errmess = ""       - сообщение об ошибке - пустая строка
#       self.rank               - числовая оценка качества кредита по шкале от 0 до 10
#       self.interest_discounted        - используем для качественной тексто-цветовой оценки в хабе (
#       self.overpaid_discounted_pc     - реальная переплата %
#       self.overpaid               - переплата номинальная
#       self.overpaid_discounted    - переплата реальная (с учетом инфляции)
#       self.annuity                - аннуитетный платеж (с учетом ежемсячных комиссий)
#       self.interest_effective     - эффективная % ставка по кредиту (с учетом комиссий)
#       self.interest_over_inflate  - превышение эффективной ставки над инфляцией

class LoanPay:

    def __init__(self, loan, periods, month, interest, inflate, comiss, insurance, decimal=2):
        erst = ""  # строковый идентификатор стадий расчетов / места фиксации ошибки (для блока Except)
        try:
            # Устанавливаем корректное значение периодов выплаты (всегда = 1 мес), если выбран год надо *12
            erst = "check period is month"
            if not month:
                periods = periods * 12  # если выбран годовой формат данных, умножаем количество месяцев

            # Расчитываем величину ежемесячной инфляции, исходя из данных о годовой инфляции в долях целого
            erst = "calculate month inflation, interest and float payment"
            years = periods / 12  # срок кредита в годах
            inflate_month_abs = (1 + inflate / 100) ** (1 / 12) - 1
            interest_pc_per_month = interest / 100 / 12  # перевод годовых процентов в ежемесячные
            inflate_month_discount = 1 / (1 + inflate_month_abs)  # коэф. дисконтирования к предыдущему месяца
            payment_month = loan * (interest_pc_per_month + interest_pc_per_month /
                                    ((1 + interest_pc_per_month) ** periods - 1)) + comiss
            payment_total = (payment_month + insurance / 12) * periods  # добавляем ежегодный страховой платеж

            # Расчет дисконтированных денежных потоков
            erst = "calculate discounted payment"
            payment_total_discount = 0  # инициируем переменную сумма всех платежей, дисконтированная
            for theperiod in range(1, periods + 1):
                month_discount = inflate_month_discount ** theperiod  # коэффициент дисконтирования для текущего месяца
                payment_month_discount = payment_month * month_discount  # дисконтированный платеж в текущем месяце
                payment_total_discount += payment_month_discount  # суммируем дисконтированный результат

            # Расчет переплаты
            erst = "calculate overpaid"
            overpaid = payment_total - loan  # переплата номинальная
            comiss_total = (comiss + insurance / 12) * periods  # суммарный размер уплаченных комиссий
            overpaid_discounted = payment_total_discount - loan  # переплата реальная (с учетом инфляции)
            overpaid_discounted_pc = overpaid_discounted / loan * 100  # переплата реальная , % от кредита

            # Расчет комиссий и ее веса в платежах
            erst = "calculate commissions"
            comiss_abs = (1 + comiss_total / loan) ** (1 / years)  # размер комиссий по отношению к сумме долга, в долях
            comiss_pc = (comiss_abs - 1) * 100  # размер комиссий по отношению к сумме долга, в %
            interest_effective = interest + comiss_pc  # эффективная % ставка по кредиту (с учетом комиссий)

            # Эффективная ставка и качество кредита
            erst = "asses quality"
            eff_interest_discount_pc = interest_effective - inflate  # базовый параметр для оценки качества кредита
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

            # РАСЧЕТ ЗАВЕРШИЛСЯ УДАЧНО, ЕСЛИ ЗДЕСЬ, создаем необходимые свойства класса
            erst = "make properties"
            self.rank = round(rank, 1)  # числовая оценка качества кредита по шкале от 0 до 10
            self.interest_discounted = round(eff_interest_discount_pc, 1)  # используем для вербально-цветовой оценки
            self.overpaid_discounted_pc = round(overpaid_discounted_pc, 1)  # реальная переплата %
            self.overpaid = round(overpaid, decimal)  # переплата номинальная
            self.overpaid_discounted = round(overpaid_discounted, decimal)  # переплата реальная (с учетом инфляции)
            self.annuity = round(payment_month, decimal)  # аннуитетный платеж (с учетом ежемсячных комиссий)
            self.interest_effective = round(interest_effective,
                                            1)  # эффективная % ставка по кредиту (с учетом комиссий)
            self.interest_over_inflate = round(eff_interest_discount_pc,
                                               1)  # превышение эффективной ставки над инфляцией

            self.errmess = ""  # ошибки нет, делаем сообщение об ошибке пустым полем
            self.errors = False  # флаг отсутствия ошибки

        except Exception:
            self.errors = True  # сигнализируем о неудачной попытке расчета
            self.errmess = erst  # сохраняем сообщение о стадии, где была обнаружена ошибка
