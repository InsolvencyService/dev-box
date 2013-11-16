def comparable_values(claim):
    values = {}
    mappings = {
        'gross_rate_of_pay': 'employee_basic_weekly_pay'
    }

    for claimant_key, employee_key in mappings.items():
        values.update(
            {claimant_key: (claim[0][claimant_key],claim[1][employee_key])}
        )

    return values

