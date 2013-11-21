def comparable_values(claim):
    claimant_values, employee_record_values = claim
    mappings = {
        'gross_rate_of_pay': 'employee_basic_weekly_pay',
        'gross_amount_owed': 'employee_owed_wages_in_arrears'
    }
    compare = {}
    for key in mappings.keys():
        if key in claimant_values.keys():
            compare[key] =  mappings[key]
    return {k: (claimant_values[k],employee_record_values[v]) for k, v in compare.iteritems()}

