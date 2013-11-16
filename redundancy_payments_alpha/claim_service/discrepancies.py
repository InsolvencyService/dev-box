def comparable_values(claim):
    claimant_values, employee_record_values = claim
    mappings = {
        'gross_rate_of_pay': 'employee_basic_weekly_pay'
    }
    return {k: (claimant_values[k],employee_record_values[v]) for k, v in mappings.iteritems()}

