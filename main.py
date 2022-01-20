from calcl import LoanPay as Lp

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

if __name__ == '__main__':
    print_hi()

