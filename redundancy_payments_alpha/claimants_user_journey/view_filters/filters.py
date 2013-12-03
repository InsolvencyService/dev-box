def discrepancy_message(discrepancy):
    return 'The value you provided was %s but the insolvency ' \
           'practitioner handling this case ' \
           'suggested %s.' % (discrepancy[0], discrepancy[1])

def summary_message(discrepancy):
    return 'The Insolvency Practitioner has suggested 950. Your payment will be calculated using the lower figure of 950'


def setup_filters(app):
    app.jinja_env.filters['discrepancy_message'] = discrepancy_message
