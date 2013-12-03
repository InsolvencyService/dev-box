def discrepancy_message(discrepancy):
    return 'The value you provided was %s but the insolvency ' \
           'practitioner handling this case ' \
           'suggested %s.' % (discrepancy[0], discrepancy[1])

def summary_message(discrepancy):
    cl_value = discrepancy[0]
    ip_value = discrepancy[1]
    if ip_value < cl_value:
        return 'The Insolvency Practitioner has suggested %s. ' \
               'Your payment will be calculated using the ' \
               'lower figure of %s' % (ip_value, ip_value)
    else:
        return 'You have suggested %s. ' \
               'Your payment will therefore be calculated using the ' \
               'lower figure of %s' % (cl_value, cl_value)


def setup_filters(app):
    app.jinja_env.filters['discrepancy_message'] = discrepancy_message
    app.jinja_env.filters['summary_message'] = summary_message
