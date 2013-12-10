from decimal import Decimal

def yearly_to_weekly_gross_rate_of_pay(details):
    amount = details['gross_pay']
    weekly_gross_rate_of_pay = (Decimal(amount) / 365)*7
    rounding = Decimal('0.01')
    return str(weekly_gross_rate_of_pay.quantize(rounding))

