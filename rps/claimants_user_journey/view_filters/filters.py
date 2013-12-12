def discrepancy_message(discrepancy):
    return 'The value you provided was %s but the insolvency ' \
           'practitioner handling this case ' \
           'suggested %s.' % (discrepancy[0], discrepancy[1])

def summary_message(discrepancy):
    cl_value = discrepancy[0]
    ip_value = discrepancy[1]

    cl_value = cl_value.replace('"', '')
    ip_value = ip_value.replace('"', '')

    if float(ip_value) < float(cl_value):
        return 'The Insolvency Practitioner has suggested %s. ' \
               'Your payment will be calculated using the ' \
               'lower figure of %s' % (ip_value, ip_value)
    else:
        return 'You have suggested %s. ' \
               'Your payment will be calculated using the ' \
               'lower figure of %s' % (cl_value, cl_value)


def date_summary(date_list):
    return "%s/%s/%s" % (
        date_list[0],
        date_list[1],
        date_list[2]
    )


def setup_filters(app):
    app.jinja_env.filters['discrepancy_message'] = discrepancy_message
    app.jinja_env.filters['summary_message'] = summary_message
    app.jinja_env.filters['date_summary'] = date_summary
