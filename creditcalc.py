import argparse
import math
import sys

parser = argparse.ArgumentParser(description='Loan Calculator')
parser.add_argument('--type', choices=['annuity', 'diff'],
                    help='type of payment')
parser.add_argument('--payment', type=int,
                    help='monthly payment amount')
parser.add_argument('--principal', type=float,
                    help='loan principal')
parser.add_argument('--periods', type=int,
                    help='number of months')
parser.add_argument('--interest', type=float, default=0,
                    help='specified without a percent sign')

args = parser.parse_args()
list_args = sys.argv
interest_nom = args.interest / (12 * 100)
m = 1
overpayment_count = 0
error_mess = 'Incorrect parameters'

def diff_payments():
    answer = (args.principal / args.periods) \
             + interest_nom * (args.principal
                               - ((args.principal * (m - 1))
                                  / args.periods))
    return math.ceil(answer)

def monthly_payment():
    answer = args.principal \
                      * (interest_nom * math.pow(1 + interest_nom, args.periods)) \
                      / (math.pow(1 + interest_nom, args.periods) - 1)
    return math.ceil(answer)

def loan_principal():
    answer = args.payment \
                     / ((interest_nom * math.pow(1 + interest_nom, args.periods))
                        / (math.pow(1 + interest_nom, args.periods) - 1))
    return math.floor(answer)

def number_months():
    x = args.payment / (args.payment - interest_nom * args.principal)
    base = 1 + interest_nom
    number_months = math.ceil(math.log(x, base))
    return math.ceil(number_months)

if (args.type == None or args.type not in ['diff', 'annuity'] )\
    or (args.type == 'diff' and args.payment != None)\
    or (args.interest == 0)\
    or (len(list_args) != 5):
        print(error_mess)
elif args.type == 'diff':
    if args.principal < 0 or args.periods < 0 or args.interest < 0:
        print(error_mess)
    else:
        for pay_month in range(args.periods):
            pay_month = diff_payments()
            print(f'Month {m}: payment is {pay_month}')
            m += 1
            overpayment_count += pay_month
        print(f'Overpayment = {math.ceil(overpayment_count - args.principal)}')
elif args.type == 'annuity':
    if args.payment == None:
        if args.principal < 0 or args.interest < 0 or args.periods < 0:
            print(error_mess)
        else:
            monthly_payment = monthly_payment()
            print(f'Your annuity payment = {monthly_payment}!')
            overpayment = (monthly_payment * args.periods) - args.principal
    elif args.principal == None:
        if args.payment < 0 or args.periods < 0 or args.interest < 0:
            print(error_mess)
        else:
            loan_principal = loan_principal()
            print(f'Your loan principal = {loan_principal}!')
            overpayment = (args.payment * args.periods) - loan_principal
    elif args.periods == None:
        if args.payment < 0 or args.principal < 0 or args.interest < 0:
            print(error_mess)
        else:
            number_months = number_months()
            if number_months < 12:
                if number_months == 1:
                    print('It will take 1 month to repay this loan!')
                else:
                    print(f'It will take {number_months} months to repay this loan!')
            elif number_months == 12:
                print('It will take 1 year to repay this loan!')
            elif number_months > 12:
                if number_months % 12 == 0:
                    years = number_months // 12
                    print(f'It will take {years} years to repay this loan!')
                else:
                    years = number_months // 12
                    months = number_months % 12
                    if months == 1:
                        print(f'It will take {years} years and {months} month to repay this loan!')
                    elif years == 1 and months == 1:
                        print(f'It will take {years} year and {months} month to repay this loan!')
                    elif years == 1:
                        print(f'It will take {years} year and {months} months to repay this loan!')
                    else:
                        print(f'It will take {years} years and {months} months to repay this loan!')
            overpayment = (args.payment * number_months) - args.principal
    print(f'Overpayment = {math.ceil(overpayment)}')